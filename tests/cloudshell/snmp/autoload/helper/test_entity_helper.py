from unittest.mock import Mock, create_autospec

from cloudshell.snmp.autoload.constants.entity_constants import (
    CHASSIS_MATCH_PATTERN,
    ENTITY_VENDOR_TYPE_TO_CLASS_MAP,
)
from cloudshell.snmp.autoload.helper.entity_helper import EntityHelper
from cloudshell.snmp.autoload.snmp.entities.snmp_entity_base import BaseEntity

"""
Code Analysis:
--The EntityHelper class is responsible for determining the physical class of a given entity.
- The get_physical_class method takes an entity object as input and returns a string representing the physical class of the entity.
- The method first checks if the entity matches a container pattern, in which case it returns "container".
- If the entity does not match the container pattern, it checks the entity's class. If the class is not defined or is "other", it attempts to determine the class based on the entity's vendor type.
- If the vendor type matches a known pattern in the ENTITY_VENDOR_TYPE_TO_CLASS_MAP, the corresponding class is returned.
- If none of the above conditions are met, the method returns the entity's class.
- The class imports constants from the cloudshell.snmp.autoload package and extends the BaseEntity class from the snmp_entity_base module.
- The ENTITY_TO_CONTAINER_PATTERN and ENTITY_VENDOR_TYPE_TO_CLASS_MAP constants are used to match vendor types to physical classes.
- Overall, the EntityHelper class provides a convenient way to determine the physical class of an entity based on its vendor type and other attributes.
"""

"""
Test Plan:
- test_get_physical_class_entity_matches_container_pattern(): tests that the method returns "container" when the entity matches a container pattern. Tags: [happy path]
- test_get_physical_class_entity_class_defined_and_matches_known_physical_class(): tests that the method returns the correct physical class when the entity class is defined and matches a known physical class. Tags: [happy path]
- test_get_physical_class_entity_class_not_defined(): tests that the method determines the physical class based on the vendor type when the entity class is not defined. Tags: [edge case]
- test_get_physical_class_entity_class_is_other(): tests that the method determines the physical class based on the vendor type when the entity class is "other". Tags: [edge case]
- test_get_physical_class_entity_vendor_type_does_not_match_known_physical_class(): tests that the method returns the entity class when the entity vendor type does not match a known physical class. Tags: [general behavior]
- test_get_physical_class_entity_vendor_type_matches_known_physical_class(): tests that the method returns the correct physical class when the entity vendor type matches a known physical class. Tags: [happy path]
- test_get_physical_class_entity_vendor_type_is_defined_but_does_not_match_known_physical_class(): tests that the method returns the entity class when the entity vendor type is defined but does not match a known physical class. Tags: [general behavior]
- test_get_physical_class_entity_does_not_match_container_pattern_and_physical_class_cannot_be_determined(): tests that the method returns an empty string when the entity does not match a container pattern and the physical class cannot be determined. Tags: [edge case]
"""


class TestEntityHelper:
    def test_get_physical_class_entity_defined_and_matches_container(self):
        # Arrange
        expected_result = "container"
        entity = create_autospec(BaseEntity)
        entity.entity_class = "container"
        entity.vendor_type = "1.1"

        # Act
        result = EntityHelper().get_physical_class(entity)

        # Assert
        assert result == expected_result

    def test_get_physical_class_entity_class_defined_and_matches_known_physical_class(
        self,
    ):
        # Arrange
        entity = create_autospec(BaseEntity)
        entity.entity_class = "chassis"
        entity.vendor_type = "1.1"

        # Act
        result = EntityHelper().get_physical_class(entity)

        # Assert
        assert result == "chassis"

    def test_get_physical_class_entity_class_not_defined(self):
        # Arrange
        entity = create_autospec(BaseEntity)
        entity.entity_class = ""
        expected_result = "chassis"
        entity.vendor_type = f"UnknownDevice{expected_result.title()}"

        # Act
        result = EntityHelper().get_physical_class(entity)

        # Assert
        assert result == expected_result

    def test_get_physical_class_entity_class_is_other(self):
        # Arrange
        expected_result = "module"
        entity = create_autospec(BaseEntity)
        entity.entity_class = "other"
        entity.vendor_type = f"UnknownDevice{expected_result.title()}"

        # Act
        result = EntityHelper().get_physical_class(entity)

        # Assert
        assert result == expected_result

    def test_get_physical_class_entity_vendor_type_does_not_match_known_physical_class(
        self,
    ):
        # Arrange
        expected_result = ""
        entity = create_autospec(BaseEntity)
        entity.entity_class = ""
        entity.vendor_type = f"UnknownDevice{expected_result.title()}"

        # Act
        result = EntityHelper().get_physical_class(entity)

        # Assert
        assert result == entity.entity_class

    def test_get_physical_class_entity_vendor_type_matches_known_physical_class(self):
        # Arrange
        entity = Mock(spec=BaseEntity, vendor_type="cevChassis", entity_class="")

        # Act
        result = EntityHelper().get_physical_class(entity)

        # Assert
        assert result == ENTITY_VENDOR_TYPE_TO_CLASS_MAP[CHASSIS_MATCH_PATTERN]

    def test_get_phys_cl_ent_vendor_type_is_defined_does_not_match_known_physical_class(
        self,
    ):
        # Arrange
        entity = Mock(spec=BaseEntity, vendor_type="cevUnknown", entity_class="chassis")

        # Act
        result = EntityHelper().get_physical_class(entity)

        # Assert
        assert result == entity.entity_class

    def test_get_phys_cl_physical_class_cannot_be_determined(
        self,
    ):
        # Arrange
        entity = Mock(spec=BaseEntity, vendor_type="cevUnknown", entity_class="")

        # Act
        result = EntityHelper().get_physical_class(entity)

        # Assert
        assert result == ""
