from unittest.mock import Mock

MOCK_BAD_CHASSIS_SNMP_RESPONSE = {
    "1": {
        "entPhysicalParentRelPos": Mock(safe_value="-1"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco 2500 Series Wireless LAN Controller"
        ),
        "entPhysicalName": Mock(safe_value="Chassis"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value=""),
        "entPhysicalVendorType": Mock(safe_value=""),
        "entPhysicalModelName": Mock(safe_value="AIR-CT2504-K9"),
        "entPhysicalSerialNum": Mock(safe_value="PSZ19201CDR"),
        "entPhysicalSoftwareRev": Mock(safe_value="8.2.100.0"),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "8": {
        "entPhysicalParentRelPos": Mock(safe_value="-1"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Aironet 3700 Series (IEEE 802.11ac) Access Point"
        ),
        "entPhysicalName": Mock(safe_value="AP3700"),
        "entPhysicalContainedIn": Mock(safe_value="0"),
        "entPhysicalClass": Mock(safe_value=""),
        "entPhysicalVendorType": Mock(safe_value=""),
        "entPhysicalModelName": Mock(safe_value="AIR-CAP3702I-A-K9"),
        "entPhysicalSerialNum": Mock(safe_value="FCW1925NA7E"),
        "entPhysicalSoftwareRev": Mock(safe_value="8.2.100.0"),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
}
