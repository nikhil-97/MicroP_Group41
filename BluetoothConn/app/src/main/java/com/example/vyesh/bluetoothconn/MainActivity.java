package com.example.vyesh.bluetoothconn;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ArrayAdapter;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class MainActivity extends AppCompatActivity {
    Button scan_button;
    ListView pairedDevicesList;
    private BluetoothAdapter BA;
    private Set<BluetoothDevice>pairedDevices;
    private List<DevicesList> devicesList = new ArrayList<>();
    private boolean ConnectionThreadStatus;
    static ConnectionThread thread;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        scan_button = (Button) findViewById(R.id.scan_button);
        pairedDevicesList = (ListView)findViewById(R.id.listView);
        BA = BluetoothAdapter.getDefaultAdapter();
        final Context context = getApplicationContext();

        pairedDevicesList.setOnItemClickListener(new AdapterView.OnItemClickListener(){
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id)
            {
                DevicesList currentDevice = devicesList.get(position);
                String CurrentMacAddress = currentDevice.getMacAddress();
                thread = new ConnectionThread(CurrentMacAddress, context, BA);
                ConnectionThreadStatus = thread.sockectConnection();
               if(ConnectionThreadStatus)
               {
                   Intent intent = new Intent(MainActivity.this, ControllerActivity.class);
                   intent.putExtra("MacAddress", CurrentMacAddress);
                   startActivity(intent);
               }
            }
        });

    }

    public void  turnOn(View v)
    {
        if(!BA.isEnabled())
        {
            Intent turnOn = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(turnOn, 0);
            Toast.makeText(getApplicationContext(), "Turned On", Toast.LENGTH_SHORT).show();
        }
        else
        {
            Toast.makeText(getApplicationContext(), "Already On", Toast.LENGTH_SHORT).show();
        }
    }

    public void scanPairedDevices(View v)
    {
        pairedDevices = BA.getBondedDevices();
        devicesList.clear();

        for(BluetoothDevice bt: pairedDevices)
        {
            devicesList.add(new DevicesList(bt.getName(), bt.getAddress()));
        }
        Toast.makeText(getApplicationContext(), "Showing Paired Devices", Toast.LENGTH_SHORT).show();

        ArrayAdapter<DevicesList> adapter = new DevicesListAdapter();
        pairedDevicesList.setAdapter(adapter);
    }


    public class DevicesListAdapter extends ArrayAdapter<DevicesList>
    {
        public DevicesListAdapter() {
            super(MainActivity.this, R.layout.my_layout, devicesList);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            if(convertView == null)
            {
                convertView = getLayoutInflater().inflate(R.layout.my_layout, parent, false);
            }

            DevicesList myCurrentDevice = devicesList.get(position);

            TextView deviceName = (TextView) convertView.findViewById(R.id.deviceName);

            deviceName.setText(myCurrentDevice.getDeviceName());

            return convertView;
        }
    }
}
