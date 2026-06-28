from engine.ble_backend import (
    BleAdvertisement,
    BleCharacteristic,
    BleService,
    service_characteristic_map,
)


def test_ble_service_characteristic_map():
    notify_char = BleCharacteristic(
        uuid="00002ad1-0000-1000-8000-00805f9b34fb",
        properties=("notify",),
    )
    read_char = BleCharacteristic(
        uuid="00002acc-0000-1000-8000-00805f9b34fb",
        properties=("read",),
    )
    service = BleService(
        uuid="00001826-0000-1000-8000-00805f9b34fb",
        characteristics=(notify_char, read_char),
    )

    mapped = service_characteristic_map(service)

    assert mapped[notify_char.uuid] is notify_char
    assert mapped[read_char.uuid] is read_char


def test_ble_advertisement_is_immutable_data():
    adv = BleAdvertisement(
        local_name="ProjectAtlas",
        service_uuids=("00001826-0000-1000-8000-00805f9b34fb",),
    )

    assert adv.local_name == "ProjectAtlas"
    assert adv.service_uuids == ("00001826-0000-1000-8000-00805f9b34fb",)
