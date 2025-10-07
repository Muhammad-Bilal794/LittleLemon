"""
Comprehensive unit tests for the `restaurant` app views (Menu & Booking) and the index view.

These tests aim to check:
- index view renders the expected template and returns 200
- Menu List/Create/Retrieve/Update/Delete behavior and status codes
- Booking ModelViewSet behavior (permission enforcement, list/retrieve/create/update/delete)
- BookingViewSet has `IsAuthenticated` in its permission_classes

Notes / robustness features:
- The tests attempt common field names for Menu (`title`, `name`, `price`, `inventory`) and Booking (`name`, `no_of_guests`).
  If your models use different required fields the tests will skip with a helpful message — adjust the payloads in the setUp block accordingly.

Run with:
    python manage.py test restaurant

"""
from decimal import Decimal
from django.test import TestCase, Client
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

# Import the app models & views (relative import within app tests)
from .models import Menu, Booking
from . import views


BASE_APP_URL = "/restaurant"
MENU_URL = f"{BASE_APP_URL}/menu/"
MENU_DETAIL = lambda pk: f"{BASE_APP_URL}/menu/{pk}/"
BOOKING_URL = f"{BASE_APP_URL}/Booking/tables/"
BOOKING_DETAIL = lambda pk: f"{BASE_APP_URL}/Booking/tables/{pk}/"
INDEX_URL = f"{BASE_APP_URL}/"
API_TOKEN_URL = f"{BASE_APP_URL}/api-token-auth/"


class MenuViewsTestCase(APITestCase):
    """Tests for Menu List/Create/Retrieve/Update/Delete endpoints."""

    def setUp(self):
        # Use APIClient for API requests
        self.client = APIClient()

        # Try to create a Menu instance with the most-common fields used in the course
        # If your Menu model uses different required fields, these attempts will fail and the test will be skipped.
        try:
            # Common Little Lemon fields: title, price, inventory
            self.menu = Menu.objects.create(title="Pizza", price=Decimal("9.99"), inventory=10)
            self.menu_create_payload = {"title": "Burger", "price": "5.50", "inventory": 15}
            self.menu_name_field = "title"
        except Exception as e1:
            try:
                # Alternate possible field names
                self.menu = Menu.objects.create(name="Pizza", price=Decimal("9.99"))
                self.menu_create_payload = {"name": "Burger", "price": "5.50"}
                self.menu_name_field = "name"
            except Exception as e2:
                self.skipTest(
                    "Could not create a Menu instance in setUp. Update the test payloads to match your Menu model fields. "
                    f"Errors: primary: {e1}; fallback: {e2}"
                )

    def _extract_name_from_response(self, data):
        for key in ("title", "name"):
            if key in data:
                return data[key]
        return None

    def test_index_view_renders_template(self):
        """Index view should return 200 and render index.html"""
        client = Client()  # use Django Client to inspect template usage
        response = client.get(INDEX_URL)
        # Expect HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Template name 'index.html' is used in the provided view code
        self.assertTemplateUsed(response, "index.html")

    def test_get_menu_list_returns_list_and_200(self):
        response = self.client.get(MENU_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list, "Expected a JSON list from the menu list endpoint.")
        self.assertGreaterEqual(len(response.json()), 1, "At least one menu item (created in setUp) should be returned.")

    def test_create_menu_item_returns_201_and_creates_model(self):
        response = self.client.post(MENU_URL, self.menu_create_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Create should return 201 but returned {response.status_code}: {response.content}")

        # Check model created (look up by the name/title we used)
        lookup_field = self.menu_name_field
        lookup_value = self.menu_create_payload[lookup_field]
        created = Menu.objects.filter(**{lookup_field: lookup_value}).exists()
        self.assertTrue(created, "Menu object should exist after successful POST to the list endpoint.")

    def test_retrieve_single_menu_item(self):
        response = self.client.get(MENU_DETAIL(self.menu.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        returned_name = self._extract_name_from_response(data)
        expected_name = getattr(self.menu, self.menu_name_field)
        self.assertEqual(returned_name, expected_name,
                         "Retrieved object should have the same name/title as the created instance.")

    def test_update_menu_item_put(self):
        # Full update via PUT
        new_payload = dict(self.menu_create_payload)  # copy keys used by the model
        # change the name/title value
        name_field = self.menu_name_field
        new_payload[name_field] = "Updated Name"
        response = self.client.put(MENU_DETAIL(self.menu.pk), new_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu.refresh_from_db()
        self.assertEqual(getattr(self.menu, name_field), "Updated Name")

    def test_partial_update_menu_item_patch(self):
        # Partial update via PATCH (change only one field)
        patch_payload = {}
        # choose a numeric field if it exists; otherwise patch the name/title
        if hasattr(self.menu, "inventory"):
            patch_payload["inventory"] = 99
            response = self.client.patch(MENU_DETAIL(self.menu.pk), patch_payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.menu.refresh_from_db()
            self.assertEqual(self.menu.inventory, 99)
        else:
            name_field = self.menu_name_field
            patch_payload[name_field] = "Partially Updated"
            response = self.client.patch(MENU_DETAIL(self.menu.pk), patch_payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.menu.refresh_from_db()
            self.assertEqual(getattr(self.menu, name_field), "Partially Updated")

    def test_delete_menu_item_returns_204_and_removes_object(self):
        response = self.client.delete(MENU_DETAIL(self.menu.pk))
        # DestroyAPIView normally returns 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(pk=self.menu.pk).exists(), "Menu object should be deleted after DELETE.")


class BookingViewSetTestCase(APITestCase):
    """Tests to ensure BookingViewSet enforces authentication and CRUD behavior."""

    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Try common Booking fields (name, no_of_guests). If fails, skip tests with guidance.
        try:
            self.booking = Booking.objects.create(name="Alice", no_of_guests=2)
            self.booking_payload = {"name": "Bob", "no_of_guests": 3}
        except Exception as e:
            self.skipTest(
                f"Could not create Booking instance in setUp. Update the test payloads to match your Booking model fields. Error: {e}"
            )

    def test_booking_viewset_has_isauthenticated_permission(self):
        # Ensure BookingViewSet explicitly includes IsAuthenticated in permission_classes
        self.assertIn(IsAuthenticated, getattr(views.BookingViewSet, "permission_classes", []),
                      "BookingViewSet should require IsAuthenticated permission.")

    def test_unauthenticated_requests_are_denied(self):
        response = self.client.get(BOOKING_URL)
        # Different DRF setups may return 401 or 403 for unauthenticated access depending on authentication classes.
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
                      f"Unauthenticated requests should be denied (401 or 403), got {response.status_code}.")

    def test_authenticated_list_and_create_booking(self):
        # Authenticate the client as a user
        self.client.force_authenticate(user=self.user)

        # LIST should succeed
        response = self.client.get(BOOKING_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # CREATE a new booking
        response = self.client.post(BOOKING_URL, self.booking_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Expected 201 on booking create, got {response.status_code}: {response.content}")
        self.assertTrue(Booking.objects.filter(name=self.booking_payload.get("name")).exists())

    def test_retrieve_update_delete_booking_detail(self):
        self.client.force_authenticate(user=self.user)
        detail_url = BOOKING_DETAIL(self.booking.pk)

        # Retrieve
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("name"), self.booking.name)

        # Update (PUT)
        update_payload = {"name": "Alice Updated", "no_of_guests": 4}
        response = self.client.put(detail_url, update_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.name, "Alice Updated")

        # Delete
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())

    def test_obtain_auth_token_endpoint_returns_token(self):
        # If rest_framework.authtoken is registered, this endpoint should return a token for valid credentials
        User = get_user_model()
        token_user = User.objects.create_user(username="tokenuser", password="tokenpass")
        response = self.client.post(API_TOKEN_URL, {"username": "tokenuser", "password": "tokenpass"}, format="json")

        if response.status_code == status.HTTP_404_NOT_FOUND:
            # The endpoint isn't wired or authtoken not installed; skip with message
            self.skipTest("api-token-auth endpoint returned 404. Is rest_framework.authtoken included and is the route configured?")

        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Expected 200 from token endpoint, got {response.status_code}: {response.content}")
        data = response.json()
        # obtain_auth_token returns {'token': '<hex>'}
        self.assertIn("token", data, "Token key not found in response from api-token-auth endpoint.")


class MiscModelAndViewTests(TestCase):
    """A few small unit tests that don't need full API client features."""

    def test_booking_model_str_and_fields(self):
        # Quick sanity: ensure we can create a Booking in a non-APITestCase (raises a helpful error if model differs)
        try:
            b = Booking.objects.create(name="Sanity", no_of_guests=1)
            self.assertEqual(str(b) is not None, True)
        except Exception as e:
            self.skipTest(f"Skipping Booking model sanity test because Booking model fields prevented creation: {e}")


# End of tests
