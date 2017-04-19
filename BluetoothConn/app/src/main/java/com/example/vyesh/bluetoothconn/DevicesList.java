package com.example.vyesh.bluetoothconn;

public class DevicesList {
    private String deviceName;
    private String macAddress;

    public DevicesList(String deviceName, String macAddress)
    {
        this.deviceName = deviceName;
        this.macAddress = macAddress;
    }

    public String getDeviceName()
    {
        return deviceName;
    }

    public String getMacAddress()
    {
        return macAddress;
    }
}
