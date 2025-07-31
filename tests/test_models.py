"""
Unit tests for data models.
"""

import pytest
from datetime import datetime

from app.models import (
    Article, Project, PickingOrder, Picker, MaterialCart,
    StatusEnum
)


class TestArticle:
    """Test Article model."""

    def test_article_creation(self):
        """Test creating a valid article."""
        article_data = {
            "projekt_nr": "054516",
            "abteilungsgruppe": "LOGISTIK ALLES",
            "kostenstelle": "2KF",
            "baugruppe": "919713008",
            "artikel": "388303408",
            "artikel_bezeichnung": "SPANNPRATZE GS18NIMOCR36 FLZN",
            "menge": 3,
            "einheit": "stk",
            "gewicht": 0.771,
            "lagerplatz": "23IZ022A",
            "filter": "23I",
            "bestand": 596,
            "wohin": "SHL-SHV--V01",
            "lz": "",
            "lager_1_stueckliste": "MZS",
            "lager_2_bedarfslager": "MZS",
            "lager_3_referenzen": "SHL",
            "status": StatusEnum.OFFEN,
            "position": 578954208,
            "bearbeitungsart": "",
            "vorgang_id": 127099,
            "anzahl_aktion": 0
        }

        article = Article(**article_data)
        assert article.projekt_nr == "054516"
        assert article.artikel == "388303408"
        assert article.menge == 3
        assert article.gewicht == 0.771

    def test_article_total_weight(self):
        """Test total weight calculation."""
        article_data = {
            "projekt_nr": "054516",
            "abteilungsgruppe": "LOGISTIK ALLES",
            "kostenstelle": "2KF",
            "baugruppe": "919713008",
            "artikel": "388303408",
            "artikel_bezeichnung": "SPANNPRATZE GS18NIMOCR36 FLZN",
            "menge": 3,
            "einheit": "stk",
            "gewicht": 0.771,
            "lagerplatz": "23IZ022A",
            "filter": "23I",
            "bestand": 596,
            "wohin": "SHL-SHV--V01",
            "lz": "",
            "lager_1_stueckliste": "MZS",
            "lager_2_bedarfslager": "MZS",
            "lager_3_referenzen": "SHL",
            "status": StatusEnum.OFFEN,
            "position": 578954208,
            "bearbeitungsart": "",
            "vorgang_id": 127099,
            "anzahl_aktion": 0
        }

        article = Article(**article_data)
        expected_weight = 3 * 0.771
        assert article.total_weight == expected_weight

    def test_article_availability(self):
        """Test article availability calculation."""
        article_data = {
            "projekt_nr": "054516",
            "abteilungsgruppe": "LOGISTIK ALLES",
            "kostenstelle": "2KF",
            "baugruppe": "919713008",
            "artikel": "388303408",
            "artikel_bezeichnung": "SPANNPRATZE GS18NIMOCR36 FLZN",
            "menge": 3,
            "einheit": "stk",
            "gewicht": 0.771,
            "lagerplatz": "23IZ022A",
            "filter": "23I",
            "bestand": 596,
            "wohin": "SHL-SHV--V01",
            "lz": "",
            "lager_1_stueckliste": "MZS",
            "lager_2_bedarfslager": "MZS",
            "lager_3_referenzen": "SHL",
            "status": StatusEnum.OFFEN,
            "position": 578954208,
            "bearbeitungsart": "",
            "vorgang_id": 127099,
            "anzahl_aktion": 0
        }

        article = Article(**article_data)
        assert article.is_available is True

        # Test with missing quantity
        article.anzahl_fehlt = 594  # Only 2 available
        assert article.is_available is False

    def test_article_validation(self):
        """Test article validation."""
        with pytest.raises(ValueError):
            Article(
                projekt_nr="054516",
                abteilungsgruppe="LOGISTIK ALLES",
                kostenstelle="2KF",
                baugruppe="919713008",
                artikel="388303408",
                artikel_bezeichnung="SPANNPRATZE GS18NIMOCR36 FLZN",
                menge=3,
                einheit="stk",
                gewicht=-0.771,  # Negative weight should fail
                lagerplatz="23IZ022A",
                filter="23I",
                bestand=596,
                wohin="SHL-SHV--V01",
                lz="",
                lager_1_stueckliste="MZS",
                lager_2_bedarfslager="MZS",
                lager_3_referenzen="SHL",
                status=StatusEnum.OFFEN,
                position=578954208,
                bearbeitungsart="",
                vorgang_id=127099,
                anzahl_aktion=0
            )


class TestProject:
    """Test Project model."""

    def test_project_creation(self):
        """Test creating a project."""
        articles = [
            Article(
                projekt_nr="054516",
                abteilungsgruppe="LOGISTIK ALLES",
                kostenstelle="2KF",
                baugruppe="919713008",
                artikel="388303408",
                artikel_bezeichnung="SPANNPRATZE GS18NIMOCR36 FLZN",
                menge=3,
                einheit="stk",
                gewicht=0.771,
                lagerplatz="23IZ022A",
                filter="23I",
                bestand=596,
                wohin="SHL-SHV--V01",
                lz="",
                lager_1_stueckliste="MZS",
                lager_2_bedarfslager="MZS",
                lager_3_referenzen="SHL",
                status=StatusEnum.OFFEN,
                position=578954208,
                bearbeitungsart="",
                vorgang_id=127099,
                anzahl_aktion=0
            )
        ]

        project = Project(projekt_nr="054516", articles=articles)
        assert project.projekt_nr == "054516"
        assert len(project.articles) == 1
        assert project.total_articles == 1

    def test_project_total_weight(self):
        """Test project total weight calculation."""
        articles = [
            Article(
                projekt_nr="054516",
                abteilungsgruppe="LOGISTIK ALLES",
                kostenstelle="2KF",
                baugruppe="919713008",
                artikel="388303408",
                artikel_bezeichnung="SPANNPRATZE GS18NIMOCR36 FLZN",
                menge=3,
                einheit="stk",
                gewicht=0.771,
                lagerplatz="23IZ022A",
                filter="23I",
                bestand=596,
                wohin="SHL-SHV--V01",
                lz="",
                lager_1_stueckliste="MZS",
                lager_2_bedarfslager="MZS",
                lager_3_referenzen="SHL",
                status=StatusEnum.OFFEN,
                position=578954208,
                bearbeitungsart="",
                vorgang_id=127099,
                anzahl_aktion=0
            ),
            Article(
                projekt_nr="054516",
                abteilungsgruppe="LOGISTIK ALLES",
                kostenstelle="2KF",
                baugruppe="919713008",
                artikel="10813739",
                artikel_bezeichnung="DRUCKAUFNEHMER 0-750/750 BAR LSB PL:E SPF",
                menge=2,
                einheit="stk",
                gewicht=0.28,
                lagerplatz="23IZ922D",
                filter="23I",
                bestand=1024,
                wohin="SVL-SHV--V01",
                lz="",
                lager_1_stueckliste="MZS",
                lager_2_bedarfslager="MZS",
                lager_3_referenzen="SHL",
                status=StatusEnum.OFFEN,
                position=578954516,
                bearbeitungsart="",
                vorgang_id=127099,
                anzahl_aktion=0
            )
        ]

        project = Project(projekt_nr="054516", articles=articles)
        expected_weight = (3 * 0.771) + (2 * 0.28)
        assert project.total_weight == expected_weight

    def test_project_status_filtering(self):
        """Test project status filtering."""
        articles = [
            Article(
                projekt_nr="054516",
                abteilungsgruppe="LOGISTIK ALLES",
                kostenstelle="2KF",
                baugruppe="919713008",
                artikel="388303408",
                artikel_bezeichnung="SPANNPRATZE GS18NIMOCR36 FLZN",
                menge=3,
                einheit="stk",
                gewicht=0.771,
                lagerplatz="23IZ022A",
                filter="23I",
                bestand=596,
                wohin="SHL-SHV--V01",
                lz="",
                lager_1_stueckliste="MZS",
                lager_2_bedarfslager="MZS",
                lager_3_referenzen="SHL",
                status=StatusEnum.OFFEN,
                position=578954208,
                bearbeitungsart="",
                vorgang_id=127099,
                anzahl_aktion=0
            ),
            Article(
                projekt_nr="054516",
                abteilungsgruppe="LOGISTIK ALLES",
                kostenstelle="2KF",
                baugruppe="919713008",
                artikel="10813739",
                artikel_bezeichnung="DRUCKAUFNEHMER 0-750/750 BAR LSB PL:E SPF",
                menge=2,
                einheit="stk",
                gewicht=0.28,
                lagerplatz="23IZ922D",
                filter="23I",
                bestand=1024,
                wohin="SVL-SHV--V01",
                lz="",
                lager_1_stueckliste="MZS",
                lager_2_bedarfslager="MZS",
                lager_3_referenzen="SHL",
                status=StatusEnum.ABGESCHLOSSEN,
                position=578954516,
                bearbeitungsart="",
                vorgang_id=127099,
                anzahl_aktion=0
            )
        ]

        project = Project(projekt_nr="054516", articles=articles)
        assert len(project.open_articles) == 1
        assert len(project.completed_articles) == 1


class TestPickingOrder:
    """Test PickingOrder model."""

    def test_order_creation(self):
        """Test creating a picking order."""
        articles = [
            Article(
                projekt_nr="054516",
                abteilungsgruppe="LOGISTIK ALLES",
                kostenstelle="2KF",
                baugruppe="919713008",
                artikel="388303408",
                artikel_bezeichnung="SPANNPRATZE GS18NIMOCR36 FLZN",
                menge=3,
                einheit="stk",
                gewicht=0.771,
                lagerplatz="23IZ022A",
                filter="23I",
                bestand=596,
                wohin="SHL-SHV--V01",
                lz="",
                lager_1_stueckliste="MZS",
                lager_2_bedarfslager="MZS",
                lager_3_referenzen="SHL",
                status=StatusEnum.OFFEN,
                position=578954208,
                bearbeitungsart="",
                vorgang_id=127099,
                anzahl_aktion=0
            )
        ]

        project = Project(projekt_nr="054516", articles=articles)
        order = PickingOrder(order_id="ORDER-001", project=project)

        assert order.order_id == "ORDER-001"
        assert order.project.projekt_nr == "054516"
        assert order.status == StatusEnum.OFFEN
        assert order.priority == 1

    def test_order_completion(self):
        """Test order completion logic."""
        articles = [
            Article(
                projekt_nr="054516",
                abteilungsgruppe="LOGISTIK ALLES",
                kostenstelle="2KF",
                baugruppe="919713008",
                artikel="388303408",
                artikel_bezeichnung="SPANNPRATZE GS18NIMOCR36 FLZN",
                menge=3,
                einheit="stk",
                gewicht=0.771,
                lagerplatz="23IZ022A",
                filter="23I",
                bestand=596,
                wohin="SHL-SHV--V01",
                lz="",
                lager_1_stueckliste="MZS",
                lager_2_bedarfslager="MZS",
                lager_3_referenzen="SHL",
                status=StatusEnum.ABGESCHLOSSEN,
                position=578954208,
                bearbeitungsart="",
                vorgang_id=127099,
                anzahl_aktion=0
            )
        ]

        project = Project(projekt_nr="054516", articles=articles)
        order = PickingOrder(order_id="ORDER-001", project=project)

        assert order.is_complete is True
        assert order.completion_percentage == 100.0

    def test_order_completion_percentage(self):
        """Test order completion percentage calculation."""
        articles = [
            Article(
                projekt_nr="054516",
                abteilungsgruppe="LOGISTIK ALLES",
                kostenstelle="2KF",
                baugruppe="919713008",
                artikel="388303408",
                artikel_bezeichnung="SPANNPRATZE GS18NIMOCR36 FLZN",
                menge=3,
                einheit="stk",
                gewicht=0.771,
                lagerplatz="23IZ022A",
                filter="23I",
                bestand=596,
                wohin="SHL-SHV--V01",
                lz="",
                lager_1_stueckliste="MZS",
                lager_2_bedarfslager="MZS",
                lager_3_referenzen="SHL",
                status=StatusEnum.ABGESCHLOSSEN,
                position=578954208,
                bearbeitungsart="",
                vorgang_id=127099,
                anzahl_aktion=0
            ),
            Article(
                projekt_nr="054516",
                abteilungsgruppe="LOGISTIK ALLES",
                kostenstelle="2KF",
                baugruppe="919713008",
                artikel="10813739",
                artikel_bezeichnung="DRUCKAUFNEHMER 0-750/750 BAR LSB PL:E SPF",
                menge=2,
                einheit="stk",
                gewicht=0.28,
                lagerplatz="23IZ922D",
                filter="23I",
                bestand=1024,
                wohin="SVL-SHV--V01",
                lz="",
                lager_1_stueckliste="MZS",
                lager_2_bedarfslager="MZS",
                lager_3_referenzen="SHL",
                status=StatusEnum.OFFEN,
                position=578954516,
                bearbeitungsart="",
                vorgang_id=127099,
                anzahl_aktion=0
            )
        ]

        project = Project(projekt_nr="054516", articles=articles)
        order = PickingOrder(order_id="ORDER-001", project=project)

        assert order.completion_percentage == 50.0


class TestPicker:
    """Test Picker model."""

    def test_picker_creation(self):
        """Test creating a picker."""
        picker = Picker(
            picker_id="P001",
            name="John Doe",
            employee_number="EMP001"
        )

        assert picker.picker_id == "P001"
        assert picker.name == "John Doe"
        assert picker.employee_number == "EMP001"
        assert picker.is_active is True
        assert picker.total_picks_today == 0


class TestMaterialCart:
    """Test MaterialCart model."""

    def test_cart_creation(self):
        """Test creating a material cart."""
        cart = MaterialCart(
            cart_id="C001",
            capacity=500.0
        )

        assert cart.cart_id == "C001"
        assert cart.capacity == 500.0
        assert cart.current_weight == 0.0
        assert cart.is_available is True

    def test_cart_capacity_calculation(self):
        """Test cart capacity calculations."""
        cart = MaterialCart(
            cart_id="C001",
            capacity=500.0,
            current_weight=200.0
        )

        assert cart.available_capacity == 300.0
        assert cart.utilization_percentage == 40.0

    def test_cart_full_capacity(self):
        """Test cart at full capacity."""
        cart = MaterialCart(
            cart_id="C001",
            capacity=500.0,
            current_weight=500.0
        )

        assert cart.available_capacity == 0.0
        assert cart.utilization_percentage == 100.0