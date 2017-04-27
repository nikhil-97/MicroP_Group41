package com.example.vyesh.bluetoothconn;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class ControllerActivity extends AppCompatActivity
{

    private ConnectionThread currentThread = MainActivity.thread;
    private boolean readyToQuit = false;
//    private OutputStream outputStream;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_controller);

        Button left_btn = (Button) findViewById(R.id.left_btn);
        Button right_btn = (Button) findViewById(R.id.right_btn);
        Button forward_btn = (Button) findViewById(R.id.forward_btn);
        Button backward_btn = (Button) findViewById(R.id.backward_btn);
        Button vac_btn_on = (Button) findViewById(R.id.vac_btn_on);
        Button vac_btn_off = (Button) findViewById(R.id.vac_btn_off);
        Button quit_btn = (Button) findViewById(R.id.quit_btn);
        Button stop_btn = (Button) findViewById(R.id.stop_btn);
    }

    public void move(View v)
    {
        String command = v.getTag().toString();
        try
        {
            write(command);
        }
        catch (IOException e)
        {
            Toast.makeText(getApplicationContext(), "Problem Sending Data To Pi ", Toast.LENGTH_SHORT).show();
        }
        if(command.equals("q"))
        {
            if(!readyToQuit)
            {
                readyToQuit = true;
                Toast.makeText(getApplicationContext(), "Press 'quit' again to close connection", Toast.LENGTH_SHORT).show();
            }
            else if(readyToQuit)
            {
                Toast.makeText(getApplicationContext(), "Connection Closed Successfully ", Toast.LENGTH_SHORT).show();
                ControllerActivity.this.finish();
            }
        }
        else if(readyToQuit && !command.equals("q"))
        {
            readyToQuit = false;
        }
    }

    public void write(String s) throws IOException
    {
        currentThread.write(s);
    }
}

