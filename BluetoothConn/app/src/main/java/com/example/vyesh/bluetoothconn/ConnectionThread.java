package com.example.vyesh.bluetoothconn;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;
import java.io.OutputStream;
import java.util.Set;
import java.util.UUID;
import java.lang.reflect.Method;
import java.io.Serializable;


public class ConnectionThread extends Thread implements Serializable
{
    private UUID MY_UUID = UUID.fromString("0000110E-0000-1000-8000-00805F9B34FB");
    private OutputStream outputStream;
    private Context context;
    private  BluetoothSocket mmSocket;
    private  BluetoothDevice targetDevice;
    BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

    public ConnectionThread(String macAddress, Context context, BluetoothAdapter BA)
    {
        this.mBluetoothAdapter = BA;
        this.targetDevice = getBluetoothDevice(macAddress);
        Toast.makeText(context, targetDevice.getAddress(), Toast.LENGTH_SHORT).show();
        this.context = context;
        BluetoothSocket tmp = null;

        try
        {
            tmp = targetDevice.createRfcommSocketToServiceRecord(MY_UUID);
            Toast.makeText(context, "Creating Socket Successfull", Toast.LENGTH_SHORT).show();
        }
        catch (IOException e0)
        {
            Log.d("BT_TEST", "Cannot create socket");
            Toast.makeText(context, "Creating Socket failed", Toast.LENGTH_SHORT).show();
            e0.printStackTrace();
        }

        mmSocket = tmp;
    }

    private BluetoothDevice getBluetoothDevice(String macAddress)
    {
        //Get the device using the MAC Address
        Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
        BluetoothDevice targetDevice = null;
        for (BluetoothDevice device : pairedDevices)
        {
            if(device.getAddress().equals(macAddress))
            {
                targetDevice = device;
            }
        }
        return  targetDevice;
    }

    public boolean socketConnection()
    {
        boolean success;
        // Cancel discovery because it otherwise slows down the connection.
        mBluetoothAdapter.cancelDiscovery();

        try {
            // Connect to the remote device through the socket. This call blocks
            // until it succeeds or throws an exception.
            mmSocket.connect();
            success = true;
            Toast.makeText(context, "connected to device", Toast.LENGTH_SHORT).show();

        }
        catch (IOException connectException)
        {
            try
            {
                Log.e("","trying fallback...");

                mmSocket =(BluetoothSocket) targetDevice.getClass().getMethod("createRfcommSocket", new Class[] {int.class}).invoke(targetDevice,1);
                mmSocket.connect();
                outputStream = mmSocket.getOutputStream();
                success = true;

                Log.e("","Connected");
            }
            catch (Exception e2) {
                Log.e("", "Couldn't establish Bluetooth connection!");
                success = false;
            }
        }

        // The connection attempt succeeded. Perform work associated with
        // the connection in a separate thread.
        //manageMyConnectedSocket(mmSocket);
        return success;
    }

    public void cancel()
    {
        try
        {
            mmSocket.close();
        }
        catch (IOException e)
        {
            Log.e("SOCKET_CON", "Could not close the client socket", e);
        }
    }

    public void write(String s) throws IOException
    {
        outputStream.write(s.getBytes());
    }
}
