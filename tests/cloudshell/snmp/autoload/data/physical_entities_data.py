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

MOCK_SNMP_RESPONSE = {
    "4103": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 1"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 1"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2010": {
        "entPhysicalParentRelPos": Mock(safe_value="9"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 asic 2 temperature Sensor"
        ),
        "entPhysicalName": Mock(safe_value="module 6 asic 2 temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "40": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="Sensor for counting number of OK Clocks"),
        "entPhysicalName": Mock(safe_value="Sensor for counting number of OK Clocks"),
        "entPhysicalContainedIn": Mock(safe_value="11"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorClock"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4175": {
        "entPhysicalParentRelPos": Mock(safe_value="7"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 7"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 7"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4116": {
        "entPhysicalParentRelPos": Mock(safe_value="0"),
        "entPhysicalDescr": Mock(safe_value="GE LX"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver 2"),
        "entPhysicalContainedIn": Mock(safe_value="4115"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSFP1000BaseLx"
        ),
        "entPhysicalModelName": Mock(safe_value="N/A"),
        "entPhysicalSerialNum": Mock(safe_value="FNS0814R1YV"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2008": {
        "entPhysicalParentRelPos": Mock(safe_value="7"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 device-2 temperature Sensor"
        ),
        "entPhysicalName": Mock(safe_value="temperature device-2 6"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2037": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="Transceiver Port Gi6/2"),
        "entPhysicalName": Mock(safe_value="Gi6/2"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="port"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevPortBaseTEther"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4127": {
        "entPhysicalParentRelPos": Mock(safe_value="3"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 3"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 3"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2009": {
        "entPhysicalParentRelPos": Mock(safe_value="8"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 asic 1 temperature Sensor"
        ),
        "entPhysicalName": Mock(safe_value="module 6 asic 1 temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2021": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="WS-F6K-PFC3BXL Policy Feature Card 3 Rev. 1.6"
        ),
        "entPhysicalName": Mock(safe_value="switching engine sub-module of 6"),
        "entPhysicalContainedIn": Mock(safe_value="2020"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevCat6kWsf6kpfc3bxl"
        ),
        "entPhysicalModelName": Mock(safe_value="WS-F6K-PFC3BXL"),
        "entPhysicalSerialNum": Mock(safe_value="SAL09412SZ2"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4367": {
        "entPhysicalParentRelPos": Mock(safe_value="13"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 13"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 13"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2050": {
        "entPhysicalParentRelPos": Mock(safe_value="3"),
        "entPhysicalDescr": Mock(safe_value="10/100/1000BaseT"),
        "entPhysicalName": Mock(safe_value="10/100/1000BaseT Gi6/2"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="port"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevPortBaseTEther"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2018": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="module 6 RP outlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="module 6 RP outlet temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="2016"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleOutletTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "39": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="Sensor for counting number of OK VTTs"),
        "entPhysicalName": Mock(safe_value="Sensor for counting number of OK VTTs"),
        "entPhysicalContainedIn": Mock(safe_value="11"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorVtt"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "1": {
        "entPhysicalParentRelPos": Mock(safe_value="-1"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot Chassis System"
        ),
        "entPhysicalName": Mock(safe_value="CISCO7609-S"),
        "entPhysicalContainedIn": Mock(safe_value="0"),
        "entPhysicalClass": Mock(safe_value="chassis"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevChassisCisco7609S"
        ),
        "entPhysicalModelName": Mock(safe_value="CISCO7609-S"),
        "entPhysicalSerialNum": Mock(safe_value="FOX1151GS65"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value="V01}"),
    },
    "2005": {
        "entPhysicalParentRelPos": Mock(safe_value="4"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 outlet temperature Sensor"
        ),
        "entPhysicalName": Mock(safe_value="temperature outlet 6"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleOutletTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2007": {
        "entPhysicalParentRelPos": Mock(safe_value="6"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 device-1 temperature Sensor"
        ),
        "entPhysicalName": Mock(safe_value="temperature device-1 6"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot Physical Slot"
        ),
        "entPhysicalName": Mock(safe_value="Physical Slot 1"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4095": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(
            safe_value="subslot 8/0 transceiver 0 Supply Voltage Sensor"
        ),
        "entPhysicalName": Mock(
            safe_value="subslot 8/0 transceiver 0 Supply Voltage Sensor"
        ),
        "entPhysicalContainedIn": Mock(safe_value="4092"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorTransceiverVoltage"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2006": {
        "entPhysicalParentRelPos": Mock(safe_value="5"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 inlet temperature Sensor"
        ),
        "entPhysicalName": Mock(safe_value="temperature inlet 6"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleInletTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4343": {
        "entPhysicalParentRelPos": Mock(safe_value="11"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 11"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 11"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2014": {
        "entPhysicalParentRelPos": Mock(safe_value="13"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 asic 6 temperature Sensor"
        ),
        "entPhysicalName": Mock(safe_value="module 6 asic 6 temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4199": {
        "entPhysicalParentRelPos": Mock(safe_value="9"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 9"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 9"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4012": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="module 8 EARL outlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="module 8 EARL outlet temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="4010"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleOutletTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2013": {
        "entPhysicalParentRelPos": Mock(safe_value="12"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 asic 5 temperature Sensor"
        ),
        "entPhysicalName": Mock(safe_value="module 6 asic 5 temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2002": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 power-output-fail Sensor"
        ),
        "entPhysicalName": Mock(safe_value="power output-fail 6"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModulePowerOutputFail"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4355": {
        "entPhysicalParentRelPos": Mock(safe_value="12"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 12"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 12"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4151": {
        "entPhysicalParentRelPos": Mock(safe_value="5"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 5"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 5"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2000": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="WS-SUP720-3BXL 2 ports Supervisor Engine 720 Rev. 4.3"
        ),
        "entPhysicalName": Mock(safe_value="module 6"),
        "entPhysicalContainedIn": Mock(safe_value="7"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevCat6kWsSup720Base"
        ),
        "entPhysicalModelName": Mock(safe_value="WS-SUP720-3BXL"),
        "entPhysicalSerialNum": Mock(safe_value="SAL09423BGZ"),
        "entPhysicalSoftwareRev": Mock(safe_value="15.0(1)S4"),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2019": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="module 6 RP inlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="module 6 RP inlet temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="2016"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleInletTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2020": {
        "entPhysicalParentRelPos": Mock(safe_value="6"),
        "entPhysicalDescr": Mock(safe_value="Switching Engine Container"),
        "entPhysicalName": Mock(safe_value="Switching Engine Container 6"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerDaughterCard"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2011": {
        "entPhysicalParentRelPos": Mock(safe_value="10"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 asic 3 temperature Sensor"
        ),
        "entPhysicalName": Mock(safe_value="module 6 asic 3 temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "59": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="OSR-7600 Clock FRU 2 OK Sensor"),
        "entPhysicalName": Mock(safe_value="Clock 2 OK Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="58"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorClock"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "60": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="OSR-7600 Clock FRU 2 In Using Sensor"),
        "entPhysicalName": Mock(safe_value="Clock 2 In Using Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="58"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorClock"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4115": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 2"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 2"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "55": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="OSR-7600 Clock FRU 1 OK Sensor"),
        "entPhysicalName": Mock(safe_value="Clock 1 OK Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="54"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorClock"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2022": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="module 6 EARL outlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="module 6 EARL outlet temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="2021"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleOutletTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4105": {
        "entPhysicalParentRelPos": Mock(safe_value="0"),
        "entPhysicalDescr": Mock(safe_value="GigEther SPA"),
        "entPhysicalName": Mock(safe_value="GigabitEthernet8/0/1"),
        "entPhysicalContainedIn": Mock(safe_value="4104"),
        "entPhysicalClass": Mock(safe_value="port"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevPortGe"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2001": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="CPU of Switching Processor"),
        "entPhysicalName": Mock(safe_value="CPU of Switching Processor 6"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevCpuCat6kWsSup720SP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2017": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="CPU of Routing Processor"),
        "entPhysicalName": Mock(safe_value="CPU of Routing Processor 6"),
        "entPhysicalContainedIn": Mock(safe_value="2016"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevCpuCat6kWsSup720RP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "56": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="OSR-7600 Clock FRU 1 In Using Sensor"),
        "entPhysicalName": Mock(safe_value="Clock 1 In Using Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="54"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorClock"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4117": {
        "entPhysicalParentRelPos": Mock(safe_value="0"),
        "entPhysicalDescr": Mock(safe_value="GigEther SPA"),
        "entPhysicalName": Mock(safe_value="GigabitEthernet8/0/2"),
        "entPhysicalContainedIn": Mock(safe_value="4116"),
        "entPhysicalClass": Mock(safe_value="port"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevPortGe"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4379": {
        "entPhysicalParentRelPos": Mock(safe_value="14"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 14"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 14"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4094": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="subslot 8/0 transceiver 0 Temperature Sensor"
        ),
        "entPhysicalName": Mock(
            safe_value="subslot 8/0 transceiver 0 Temperature Sensor"
        ),
        "entPhysicalContainedIn": Mock(safe_value="4092"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorTransceiverTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4139": {
        "entPhysicalParentRelPos": Mock(safe_value="4"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 4"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 4"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4391": {
        "entPhysicalParentRelPos": Mock(safe_value="15"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 15"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 15"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "3000": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco 7600 Series SPA Interface Processor-400 Rev. 2.5"
        ),
        "entPhysicalName": Mock(safe_value="module 7"),
        "entPhysicalContainedIn": Mock(safe_value="8"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevC6xxxSIP400"
        ),
        "entPhysicalModelName": Mock(safe_value="7600-SIP-400"),
        "entPhysicalSerialNum": Mock(safe_value="JAE11484TA2"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value="V06"),
    },
    "4093": {
        "entPhysicalParentRelPos": Mock(safe_value="0"),
        "entPhysicalDescr": Mock(safe_value="GigEther SPA"),
        "entPhysicalName": Mock(safe_value="GigabitEthernet8/0/0"),
        "entPhysicalContainedIn": Mock(safe_value="4092"),
        "entPhysicalClass": Mock(safe_value="port"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevPortGe"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "58": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="OSR-7600 Clock FRU 2"),
        "entPhysicalName": Mock(safe_value="CLK-7600 2"),
        "entPhysicalContainedIn": Mock(safe_value="57"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevClk7600"
        ),
        "entPhysicalModelName": Mock(safe_value="CLK-7600"),
        "entPhysicalSerialNum": Mock(safe_value="NWG114904SJ"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4439": {
        "entPhysicalParentRelPos": Mock(safe_value="19"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 19"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 19"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "54": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="OSR-7600 Clock FRU 1"),
        "entPhysicalName": Mock(safe_value="CLK-7600 1"),
        "entPhysicalContainedIn": Mock(safe_value="53"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevClk7600"
        ),
        "entPhysicalModelName": Mock(safe_value="CLK-7600"),
        "entPhysicalSerialNum": Mock(safe_value="NWG114904SJ"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4097": {
        "entPhysicalParentRelPos": Mock(safe_value="4"),
        "entPhysicalDescr": Mock(
            safe_value="subslot 8/0 transceiver 0 Tx Power Sensor"
        ),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver 0 Tx Power Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="4092"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorTransceiverTxPwr"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4092": {
        "entPhysicalParentRelPos": Mock(safe_value="0"),
        "entPhysicalDescr": Mock(safe_value="Unknown pluggable optics"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver 0"),
        "entPhysicalContainedIn": Mock(safe_value="4091"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSFPUnknown"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4163": {
        "entPhysicalParentRelPos": Mock(safe_value="6"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 6"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 6"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2023": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="module 6 EARL inlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="module 6 EARL inlet temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="2021"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleInletTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2015": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="MSFC Container"),
        "entPhysicalName": Mock(safe_value="MSFC Container 6"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerDaughterCard"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2012": {
        "entPhysicalParentRelPos": Mock(safe_value="11"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 asic 4 temperature Sensor"
        ),
        "entPhysicalName": Mock(safe_value="module 6 asic 4 temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4098": {
        "entPhysicalParentRelPos": Mock(safe_value="5"),
        "entPhysicalDescr": Mock(
            safe_value="subslot 8/0 transceiver 0 Rx Power Sensor"
        ),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver 0 Rx Power Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="4092"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorTransceiverRxPwr"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4104": {
        "entPhysicalParentRelPos": Mock(safe_value="0"),
        "entPhysicalDescr": Mock(safe_value="GE LX"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver 1"),
        "entPhysicalContainedIn": Mock(safe_value="4103"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSFP1000BaseLx"
        ),
        "entPhysicalModelName": Mock(safe_value="N/A"),
        "entPhysicalSerialNum": Mock(safe_value="FNS11320303"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value="0000"),
    },
    "4415": {
        "entPhysicalParentRelPos": Mock(safe_value="17"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 17"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 17"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "57": {
        "entPhysicalParentRelPos": Mock(safe_value="5"),
        "entPhysicalDescr": Mock(safe_value="Container of Clock"),
        "entPhysicalName": Mock(safe_value="Container of Clock 2"),
        "entPhysicalContainedIn": Mock(safe_value="11"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerClock"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4331": {
        "entPhysicalParentRelPos": Mock(safe_value="10"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 10"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 10"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4403": {
        "entPhysicalParentRelPos": Mock(safe_value="16"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 16"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 16"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4187": {
        "entPhysicalParentRelPos": Mock(safe_value="8"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 8"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 8"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2024": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="Transceiver Port Gi6/1"),
        "entPhysicalName": Mock(safe_value="Gi6/1"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="port"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevPortGigEthernet"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2038": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="Gigabit Transceiver Container Gi6/2"),
        "entPhysicalName": Mock(safe_value="Gigabit Transceiver Container Gi6/2"),
        "entPhysicalContainedIn": Mock(safe_value="2037"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerGbic"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4427": {
        "entPhysicalParentRelPos": Mock(safe_value="18"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 18"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 18"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4096": {
        "entPhysicalParentRelPos": Mock(safe_value="3"),
        "entPhysicalDescr": Mock(
            safe_value="subslot 8/0 transceiver 0 Bias Current Sensor"
        ),
        "entPhysicalName": Mock(
            safe_value="subslot 8/0 transceiver 0 Bias Current Sensor"
        ),
        "entPhysicalContainedIn": Mock(safe_value="4092"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorTransceiverCurrent"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2016": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="WS-SUP720 MSFC3 Daughterboard Rev. 2.3"),
        "entPhysicalName": Mock(safe_value="msfc sub-module of 6"),
        "entPhysicalContainedIn": Mock(safe_value="2015"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevCat6kWsSup720"
        ),
        "entPhysicalModelName": Mock(safe_value="WS-SUP720"),
        "entPhysicalSerialNum": Mock(safe_value="SAL09423B8L"),
        "entPhysicalSoftwareRev": Mock(safe_value="15.0(1)S4"),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2025": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="Transceiver Port Container Gi6/1"),
        "entPhysicalName": Mock(safe_value="Transceiver Port Container Gi6/1"),
        "entPhysicalContainedIn": Mock(safe_value="2024"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerGbic"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "53": {
        "entPhysicalParentRelPos": Mock(safe_value="4"),
        "entPhysicalDescr": Mock(safe_value="Container of Clock"),
        "entPhysicalName": Mock(safe_value="Container of Clock 1"),
        "entPhysicalContainedIn": Mock(safe_value="11"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerClock"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "14": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="High Speed Fan Module for CISCO7609-S 1"),
        "entPhysicalName": Mock(safe_value="FAN-MOD-9SHS 1"),
        "entPhysicalContainedIn": Mock(safe_value="13"),
        "entPhysicalClass": Mock(safe_value="fan"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevFanMod9FanTray"
        ),
        "entPhysicalModelName": Mock(safe_value="FAN-MOD-9SHS"),
        "entPhysicalSerialNum": Mock(safe_value="FOX1151GCUN"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value="V01}"),
    },
    "4": {
        "entPhysicalParentRelPos": Mock(safe_value="3"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot Physical Slot"
        ),
        "entPhysicalName": Mock(safe_value="Physical Slot 3"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "28": {
        "entPhysicalParentRelPos": Mock(safe_value="3"),
        "entPhysicalDescr": Mock(
            safe_value="power-supply 1 incompatible with fan Sensor"
        ),
        "entPhysicalName": Mock(
            safe_value="power-supply 1 incompatible with fan Sensor"
        ),
        "entPhysicalContainedIn": Mock(safe_value="20"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorPSFanIncompatible"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4001": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="module 8 power-output-fail Sensor"),
        "entPhysicalName": Mock(safe_value="power output-fail 8"),
        "entPhysicalContainedIn": Mock(safe_value="4000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModulePowerOutputFail"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "43": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="VTT-E FRU 1 OK Sensor"),
        "entPhysicalName": Mock(safe_value="VTT 1 OK Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="42"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorVtt"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "19": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="Container of Power Supply"),
        "entPhysicalName": Mock(safe_value="Container of Power Supply 1"),
        "entPhysicalContainedIn": Mock(safe_value="18"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerPowerSupply"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "5": {
        "entPhysicalParentRelPos": Mock(safe_value="4"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot Physical Slot"
        ),
        "entPhysicalName": Mock(safe_value="Physical Slot 4"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4004": {
        "entPhysicalParentRelPos": Mock(safe_value="4"),
        "entPhysicalDescr": Mock(safe_value="module 8 inlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="temperature inlet 8"),
        "entPhysicalContainedIn": Mock(safe_value="4000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleInletTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "41": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="Container of VTT"),
        "entPhysicalName": Mock(safe_value="Container of VTT 1"),
        "entPhysicalContainedIn": Mock(safe_value="11"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerVtt"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "16": {
        "entPhysicalParentRelPos": Mock(safe_value="11"),
        "entPhysicalDescr": Mock(safe_value="Container of Fan FRU"),
        "entPhysicalName": Mock(safe_value="Container of Fan FRU 2"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerFanTraySlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4003": {
        "entPhysicalParentRelPos": Mock(safe_value="3"),
        "entPhysicalDescr": Mock(safe_value="module 8 outlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="temperature outlet 8"),
        "entPhysicalContainedIn": Mock(safe_value="4000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleOutletTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "47": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="VTT-E FRU 2 OK Sensor"),
        "entPhysicalName": Mock(safe_value="VTT 2 OK Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="46"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorVtt"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "23": {
        "entPhysicalParentRelPos": Mock(safe_value="4"),
        "entPhysicalDescr": Mock(safe_value="power-supply 1 power-input Sensor"),
        "entPhysicalName": Mock(safe_value="power-supply 1 power-input Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="20"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorPSInput"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "17": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="High Speed Fan Module for CISCO7609-S 2"),
        "entPhysicalName": Mock(safe_value="FAN-MOD-9SHS 2"),
        "entPhysicalContainedIn": Mock(safe_value="16"),
        "entPhysicalClass": Mock(safe_value="fan"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevFanMod9FanTray"
        ),
        "entPhysicalModelName": Mock(safe_value="FAN-MOD-9SHS"),
        "entPhysicalSerialNum": Mock(safe_value="FOX1151GCTC"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value="V01}"),
    },
    "4005": {
        "entPhysicalParentRelPos": Mock(safe_value="5"),
        "entPhysicalDescr": Mock(safe_value="module 8 device-1 temperature Sensor"),
        "entPhysicalName": Mock(safe_value="temperature device-1 8"),
        "entPhysicalContainedIn": Mock(safe_value="4000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2003": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 insufficient cooling Sensor"
        ),
        "entPhysicalName": Mock(safe_value="switch insufficient-cooling 6"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensor"
            "ModuleInsufficientCooling"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4000": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="7600-ES20-GE3CXL ESM20G Rev. 1.1"),
        "entPhysicalName": Mock(safe_value="module 8"),
        "entPhysicalContainedIn": Mock(safe_value="9"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevC6xxxEsm20G"
        ),
        "entPhysicalModelName": Mock(safe_value="7600-ES20-GE3CXL"),
        "entPhysicalSerialNum": Mock(safe_value="JAE11495PV6"),
        "entPhysicalSoftwareRev": Mock(safe_value="15.0(1)S4"),
        "entPhysicalHardwareRev": Mock(safe_value="V02}"),
    },
    "46": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="VTT-E FRU 2"),
        "entPhysicalName": Mock(safe_value="WS-C6K-VTT-E 2"),
        "entPhysicalContainedIn": Mock(safe_value="45"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevCat6kWsc6kvtte"
        ),
        "entPhysicalModelName": Mock(safe_value="WS-C6K-VTT-E"),
        "entPhysicalSerialNum": Mock(safe_value="SMT1142H197"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "22": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="power-supply 1 power-output-fail Sensor"),
        "entPhysicalName": Mock(safe_value="power-supply 1 power-output-fail Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="20"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorPSOutput"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4002": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="module 8 insufficient cooling Sensor"),
        "entPhysicalName": Mock(safe_value="switch insufficient-cooling 8"),
        "entPhysicalContainedIn": Mock(safe_value="4000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModule"
            "InsufficientCooling"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4014": {
        "entPhysicalParentRelPos": Mock(safe_value="0"),
        "entPhysicalDescr": Mock(safe_value="Daughter Card Container"),
        "entPhysicalName": Mock(safe_value="Link Daughter Card Container 8"),
        "entPhysicalContainedIn": Mock(safe_value="4000"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerDaughterCard"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4009": {
        "entPhysicalParentRelPos": Mock(safe_value="6"),
        "entPhysicalDescr": Mock(safe_value="Switching Engine Container"),
        "entPhysicalName": Mock(safe_value="Switching Engine Container 8"),
        "entPhysicalContainedIn": Mock(safe_value="4000"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerDaughterCard"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "2004": {
        "entPhysicalParentRelPos": Mock(safe_value="3"),
        "entPhysicalDescr": Mock(
            safe_value="Supervisor module 6 fan-upgrade required Sensor"
        ),
        "entPhysicalName": Mock(safe_value="switch fanUpgrade-required 6"),
        "entPhysicalContainedIn": Mock(safe_value="2000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensor"
            "ModuleFanUpgradeRequired"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "45": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="Container of VTT"),
        "entPhysicalName": Mock(safe_value="Container of VTT 2"),
        "entPhysicalContainedIn": Mock(safe_value="11"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerVtt"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "21": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="power-supply 1 fan-fail Sensor"),
        "entPhysicalName": Mock(safe_value="power-supply 1 fan-fail Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="20"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorPSFan"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4008": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="7600-ES20-PROC FRU type (0x6005, 0x6A5(1701)) Rev. 1.1"
        ),
        "entPhysicalName": Mock(safe_value="CPU sub-module of 8"),
        "entPhysicalContainedIn": Mock(safe_value="4007"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevC6xxxEsm20GCpuDc"
        ),
        "entPhysicalModelName": Mock(safe_value="7600-ES20-PROC"),
        "entPhysicalSerialNum": Mock(safe_value="JAE11463HKZ"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4040": {
        "entPhysicalParentRelPos": Mock(safe_value="0"),
        "entPhysicalDescr": Mock(
            safe_value="module 8 Link Daughterboard temperature Sensor 0"
        ),
        "entPhysicalName": Mock(
            safe_value="module 8 Link Daughterboard temperature Sensor 0"
        ),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "44": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="VTT-E FRU 1 outlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="VTT 1 outlet temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="42"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorVtt"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "20": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="DC power supply, 4000 watt 1"),
        "entPhysicalName": Mock(safe_value="PS 1 PWR-4000-DC"),
        "entPhysicalContainedIn": Mock(safe_value="19"),
        "entPhysicalClass": Mock(safe_value="powerSupply"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevPowerSupplyDC4000W"
        ),
        "entPhysicalModelName": Mock(safe_value="PWR-4000-DC"),
        "entPhysicalSerialNum": Mock(safe_value="QCS113720C4"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value="V02}"),
    },
    "4006": {
        "entPhysicalParentRelPos": Mock(safe_value="6"),
        "entPhysicalDescr": Mock(safe_value="module 8 device-2 temperature Sensor"),
        "entPhysicalName": Mock(safe_value="temperature device-2 8"),
        "entPhysicalContainedIn": Mock(safe_value="4000"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4053": {
        "entPhysicalParentRelPos": Mock(safe_value="13"),
        "entPhysicalDescr": Mock(
            safe_value="module 8 Link Daughterboard voltage Sensor 1"
        ),
        "entPhysicalName": Mock(
            safe_value="module 8 Link Daughterboard voltage Sensor 1"
        ),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceVoltage"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "42": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="VTT-E FRU 1"),
        "entPhysicalName": Mock(safe_value="WS-C6K-VTT-E 1"),
        "entPhysicalContainedIn": Mock(safe_value="41"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevCat6kWsc6kvtte"
        ),
        "entPhysicalModelName": Mock(safe_value="WS-C6K-VTT-E"),
        "entPhysicalSerialNum": Mock(safe_value="SMT1142C592"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4055": {
        "entPhysicalParentRelPos": Mock(safe_value="15"),
        "entPhysicalDescr": Mock(
            safe_value="module 8 Link Daughterboard voltage Sensor 3"
        ),
        "entPhysicalName": Mock(
            safe_value="module 8 Link Daughterboard voltage Sensor 3"
        ),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceVoltage"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "18": {
        "entPhysicalParentRelPos": Mock(safe_value="12"),
        "entPhysicalDescr": Mock(safe_value="Container of Container of Power Supply"),
        "entPhysicalName": Mock(safe_value="Container of Container of Power Supply"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerPowerSupplyBay"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "3": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot Physical Slot"
        ),
        "entPhysicalName": Mock(safe_value="Physical Slot 2"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4041": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="module 8 Link Daughterboard temperature Sensor 1"
        ),
        "entPhysicalName": Mock(
            safe_value="module 8 Link Daughterboard temperature Sensor 1"
        ),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "13": {
        "entPhysicalParentRelPos": Mock(safe_value="10"),
        "entPhysicalDescr": Mock(safe_value="Container of Fan FRU"),
        "entPhysicalName": Mock(safe_value="Container of Fan FRU 1"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerFanTraySlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "15": {
        "entPhysicalParentRelPos": Mock(safe_value="5"),
        "entPhysicalDescr": Mock(safe_value="fan-tray 2 fan-fail Sensor"),
        "entPhysicalName": Mock(safe_value="fan-tray 2 fan-fail Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="11"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorFanTrayStatus"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4091": {
        "entPhysicalParentRelPos": Mock(safe_value="0"),
        "entPhysicalDescr": Mock(safe_value="subslot 8/0 transceiver container 0"),
        "entPhysicalName": Mock(safe_value="subslot 8/0 transceiver container 0"),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSFP"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "6": {
        "entPhysicalParentRelPos": Mock(safe_value="5"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot Physical Slot"
        ),
        "entPhysicalName": Mock(safe_value="Physical Slot 5"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4054": {
        "entPhysicalParentRelPos": Mock(safe_value="14"),
        "entPhysicalDescr": Mock(
            safe_value="module 8 Link Daughterboard voltage Sensor 2"
        ),
        "entPhysicalName": Mock(
            safe_value="module 8 Link Daughterboard voltage Sensor 2"
        ),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceVoltage"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4052": {
        "entPhysicalParentRelPos": Mock(safe_value="12"),
        "entPhysicalDescr": Mock(
            safe_value="module 8 Link Daughterboard voltage Sensor 0"
        ),
        "entPhysicalName": Mock(
            safe_value="module 8 Link Daughterboard voltage Sensor 0"
        ),
        "entPhysicalContainedIn": Mock(safe_value="4015"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleDeviceVoltage"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "11": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot backplane"
        ),
        "entPhysicalName": Mock(safe_value="Backplane"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="backplane"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevBackplaneCisco7600"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "12": {
        "entPhysicalParentRelPos": Mock(safe_value="4"),
        "entPhysicalDescr": Mock(safe_value="fan-tray 1 fan-fail Sensor"),
        "entPhysicalName": Mock(safe_value="fan-tray 1 fan-fail Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="11"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorFanTrayStatus"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4007": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="Daughter Card Container"),
        "entPhysicalName": Mock(safe_value="CPU Daughter Card Container 8"),
        "entPhysicalContainedIn": Mock(safe_value="4000"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerDaughterCard"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "49": {
        "entPhysicalParentRelPos": Mock(safe_value="3"),
        "entPhysicalDescr": Mock(safe_value="Container of VTT"),
        "entPhysicalName": Mock(safe_value="Container of VTT 3"),
        "entPhysicalContainedIn": Mock(safe_value="11"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerVtt"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4015": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="7600-ES20-20GE Link Daugher Card Rev. 1.1"
        ),
        "entPhysicalName": Mock(safe_value="LINK sub-module of 8"),
        "entPhysicalContainedIn": Mock(safe_value="4014"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevC6xxxEsm20G20x1gDc"
        ),
        "entPhysicalModelName": Mock(safe_value="7600-ES20-20GE"),
        "entPhysicalSerialNum": Mock(safe_value="JAE11474CGF"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value="N/A}"),
    },
    "10": {
        "entPhysicalParentRelPos": Mock(safe_value="9"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot Physical Slot"
        ),
        "entPhysicalName": Mock(safe_value="Physical Slot 9"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "48": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="VTT-E FRU 2 outlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="VTT 2 outlet temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="46"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorVtt"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "52": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="VTT-E FRU 3 outlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="VTT 3 outlet temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="50"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorVtt"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4010": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(
            safe_value="7600-ES20-D3CXL ESM20G Distributed Forwarding Card Rev. 1.0"
        ),
        "entPhysicalName": Mock(safe_value="switching engine sub-module of 8"),
        "entPhysicalContainedIn": Mock(safe_value="4009"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevC6xxxEsm20GPfc3CxlDc"
        ),
        "entPhysicalModelName": Mock(safe_value="7600-ES20-D3CXL"),
        "entPhysicalSerialNum": Mock(safe_value="JAE11495S76"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "29": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="Container of Power Supply"),
        "entPhysicalName": Mock(safe_value="Container of Power Supply 2"),
        "entPhysicalContainedIn": Mock(safe_value="18"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerPowerSupply"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "50": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="VTT-E FRU 3"),
        "entPhysicalName": Mock(safe_value="WS-C6K-VTT-E 3"),
        "entPhysicalContainedIn": Mock(safe_value="49"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevCat6kWsc6kvtte"
        ),
        "entPhysicalModelName": Mock(safe_value="WS-C6K-VTT-E"),
        "entPhysicalSerialNum": Mock(safe_value="SMT1142C600"),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4011": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="CPU of Distributed Forwarding Card"),
        "entPhysicalName": Mock(safe_value="CPU of Sub-Module 8 DFC Card"),
        "entPhysicalContainedIn": Mock(safe_value="4010"),
        "entPhysicalClass": Mock(safe_value="module"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevModuleCpuType"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "9": {
        "entPhysicalParentRelPos": Mock(safe_value="8"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot Physical Slot"
        ),
        "entPhysicalName": Mock(safe_value="Physical Slot 8"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "4013": {
        "entPhysicalParentRelPos": Mock(safe_value="2"),
        "entPhysicalDescr": Mock(safe_value="module 8 EARL inlet temperature Sensor"),
        "entPhysicalName": Mock(safe_value="module 8 EARL inlet temperature Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="4010"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorModuleInletTemp"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "8": {
        "entPhysicalParentRelPos": Mock(safe_value="7"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot Physical Slot"
        ),
        "entPhysicalName": Mock(safe_value="Physical Slot 7"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "51": {
        "entPhysicalParentRelPos": Mock(safe_value="1"),
        "entPhysicalDescr": Mock(safe_value="VTT-E FRU 3 OK Sensor"),
        "entPhysicalName": Mock(safe_value="VTT 3 OK Sensor"),
        "entPhysicalContainedIn": Mock(safe_value="50"),
        "entPhysicalClass": Mock(safe_value="sensor"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevSensorVtt"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
    "7": {
        "entPhysicalParentRelPos": Mock(safe_value="6"),
        "entPhysicalDescr": Mock(
            safe_value="Cisco Systems Cisco 7600 9-slot Physical Slot"
        ),
        "entPhysicalName": Mock(safe_value="Physical Slot 6"),
        "entPhysicalContainedIn": Mock(safe_value="1"),
        "entPhysicalClass": Mock(safe_value="container"),
        "entPhysicalVendorType": Mock(
            safe_value="CISCO-ENTITY-VENDORTYPE-OID-MIB::cevContainerSlot"
        ),
        "entPhysicalModelName": Mock(safe_value=""),
        "entPhysicalSerialNum": Mock(safe_value=""),
        "entPhysicalSoftwareRev": Mock(safe_value=""),
        "entPhysicalHardwareRev": Mock(safe_value=""),
    },
}
