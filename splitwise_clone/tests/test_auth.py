import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUS01LoginPage:
    def test_login_page_renders(self, page, live_server_url):
        page.goto(f"{live_server_url}/login")
        assert page.locator("h2").inner_text() == "Login"
        assert page.locator('input[name="username"]').is_visible()
        assert page.locator('input[name="password"]').is_visible()
        assert page.locator('button[type="submit"]').is_visible()

    def test_login_page_has_register_link(self, page, live_server_url):
        page.goto(f"{live_server_url}/login")
        link = page.locator("a", has_text="Register here")
        assert link.is_visible()
        assert link.get_attribute("href") == "/register"


class TestUS02LoginSuccess:
    def test_login_with_valid_credentials(self, page, live_server_url, db_users):
        page.goto(f"{live_server_url}/login")
        page.fill('input[name="username"]', "david")
        page.fill('input[name="password"]', "1234")
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server_url}/")
        assert page.locator("h2").inner_text() == "Splitwise CS50w"


class TestUS03LoginFailure:
    def test_login_with_wrong_password(self, page, live_server_url, db_users):
        page.goto(f"{live_server_url}/login")
        page.fill('input[name="username"]', "david")
        page.fill('input[name="password"]', "wrongpassword")
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server_url}/login")
        assert page.locator("text=Invalid username and/or password.").is_visible()

    def test_login_with_nonexistent_user(self, page, live_server_url, db_users):
        page.goto(f"{live_server_url}/login")
        page.fill('input[name="username"]', "nobody")
        page.fill('input[name="password"]', "1234")
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server_url}/login")
        assert page.locator("text=Invalid username and/or password.").is_visible()

    def test_login_error_shows_red_inputs(self, page, live_server_url, db_users):
        page.goto(f"{live_server_url}/login")
        page.fill('input[name="username"]', "david")
        page.fill('input[name="password"]', "wrong")
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server_url}/login")
        username_input = page.locator('input[name="username"]')
        assert "border-red-500" in username_input.get_attribute("class")


class TestUS04RegisterSuccess:
    def test_register_new_user(self, page, live_server_url, db):
        page.goto(f"{live_server_url}/register")
        page.fill('input[name="username"]', "newuser")
        page.fill('input[name="email"]', "new@example.com")
        page.fill('input[name="password"]', "pass1234")
        page.fill('input[name="confirmation"]', "pass1234")
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server_url}/")
        assert User.objects.filter(username="newuser").exists()

    def test_register_auto_login(self, page, live_server_url, db):
        page.goto(f"{live_server_url}/register")
        page.fill('input[name="username"]', "autoLogin")
        page.fill('input[name="email"]', "auto@example.com")
        page.fill('input[name="password"]', "pass1234")
        page.fill('input[name="confirmation"]', "pass1234")
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server_url}/")
        assert page.locator("h2").inner_text() == "Splitwise CS50w"


class TestUS05RegisterPasswordMismatch:
    def test_register_passwords_do_not_match(self, page, live_server_url, db):
        page.goto(f"{live_server_url}/register")
        page.fill('input[name="username"]', "testuser")
        page.fill('input[name="email"]', "test@example.com")
        page.fill('input[name="password"]', "pass1234")
        page.fill('input[name="confirmation"]', "different")
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server_url}/register")
        assert page.locator("text=Passwords must match.").is_visible()

    def test_register_mismatch_shows_error_inputs(self, page, live_server_url, db):
        page.goto(f"{live_server_url}/register")
        page.fill('input[name="username"]', "testuser")
        page.fill('input[name="email"]', "test@example.com")
        page.fill('input[name="password"]', "pass1234")
        page.fill('input[name="confirmation"]', "different")
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server_url}/register")
        pw_input = page.locator('input[name="password"]')
        assert "border-red-500" in pw_input.get_attribute("class")


class TestUS06RegisterDuplicateUsername:
    def test_register_duplicate_username(self, page, live_server_url, db_users):
        page.goto(f"{live_server_url}/register")
        page.fill('input[name="username"]', "david")
        page.fill('input[name="email"]', "other@example.com")
        page.fill('input[name="password"]', "pass1234")
        page.fill('input[name="confirmation"]', "pass1234")
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server_url}/register")
        assert page.locator("text=Username already taken.").is_visible()

    def test_register_duplicate_shows_error_on_username(
        self, page, live_server_url, db_users
    ):
        page.goto(f"{live_server_url}/register")
        page.fill('input[name="username"]', "david")
        page.fill('input[name="email"]', "other@example.com")
        page.fill('input[name="password"]', "pass1234")
        page.fill('input[name="confirmation"]', "pass1234")
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server_url}/register")
        username_input = page.locator('input[name="username"]')
        assert "border-red-500" in username_input.get_attribute("class")


class TestUS07Logout:
    @pytest.mark.skip(reason="Temporarily disabled")
    def test_logout_redirects_to_login(
        self, authenticated_page, live_server_url
    ):
        authenticated_page.goto(f"{live_server_url}/logout")
        authenticated_page.wait_for_url(f"{live_server_url}/login")
        assert authenticated_page.locator("h2").inner_text() == "Login"

    @pytest.mark.skip(reason="Temporarily disabled")
    def test_logout_destroys_session(self, authenticated_page, live_server_url):
        authenticated_page.goto(f"{live_server_url}/logout")
        authenticated_page.wait_for_url(f"{live_server_url}/login")
        authenticated_page.goto(f"{live_server_url}/")
        authenticated_page.wait_for_url(f"{live_server_url}/login**")


class TestUS20ProtectedRoutes:
    def test_index_requires_login(self, page, live_server_url):
        page.goto(f"{live_server_url}/")
        page.wait_for_url(f"{live_server_url}/login**")

    def test_create_group_requires_login(self, page, live_server_url):
        page.goto(f"{live_server_url}/create-group")
        page.wait_for_url(f"{live_server_url}/login**")

    def test_create_expense_requires_login(self, page, live_server_url):
        page.goto(f"{live_server_url}/create-expense?group_id=fake")
        page.wait_for_url(f"{live_server_url}/login**")

    def test_group_view_requires_login(self, page, live_server_url, full_db):
        group = full_db["groups"]["Vlc Apartment"]
        page.goto(f"{live_server_url}/groups/{group.id}")
        page.wait_for_url(f"{live_server_url}/login**")
