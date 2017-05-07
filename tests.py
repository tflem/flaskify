import unittest
import os

from flask_testing import TestCase
from flask import abort, url_for

from app import create_app, db
from app.models import Department, Employee, Role

class TestBase(TestCase):

    def create_app(self):
        # Pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI=
            'postgresql://postgres:@localhost/flaskify_test'
        )
        return app

    def setUp(self):
        """
        Function called before every test.
        """
        db.create_all()

        # Create test for admin user
        admin = Employee(username="admin", password="admin2017", is_admin=True)

        # Create test for non-admin users
        employee = Employee(username="paws", password="puppydog")

        # Save users to the database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Function called after every test.
        """
        db.session.remove()
        db.drop_all()

class TestModels(TestBase):

    def test_employee_model(self):
        """
        Tests number of records in Employee table.
        """
        self.assertEqual(Employee.query.count(), 2)

    def test_department_model(self):
        """
        Tests number of records in Department model.
        """

        # Create test department
        department = Department(name="IT", description="The IT Department")

        # Save department to database
        db.session.add(department)
        db.session.commit()

        self.assertEqual(Department.query.count(), 1)

    def test_role_model(self):
        """
        Tests number of records in Role table.
        """

        # Create test role
        role = Role(name="CEO", description="Run the whole show")

        # Save role to database
        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)

class TestViews(TestBase):

    def test_hompage_view(self):
        """
        Tests that homepage is accessible without login.
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Tests that login page is accessible without login.
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Tests that logout link is inaccessible without login
        and redirects to login page, then to logout.
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Tests that dashobard is inaccessible unless logged
        in and redirects to login page, then to dashboard.
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Tests that dashboard is inaccessible without login
        and redirects to login page, then to the dashboard.
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_departments_view(self):
        """
        Tests that departments page is inaccessible without
        login and redirects to login page, then to departments page.
        """
        target_url = url_for('admin.list_departments')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_roles_view(self):
        """
        Tests that roles page is inaccessible without login and
        redirects to login page, then to roles page.
        """
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_employees_view(self):
        """
        Tests that employees page is inaccessible without login
        and redirects to login page then to employees page.
        """
        target_url = url_for('admin.list_employees')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # Create route to abort request with 403 Error.
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get("/nothinghere")
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # Create route to abort request with 500 Error.
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error", response.data)

if __name__ == '__main__':
    unittest.main()
