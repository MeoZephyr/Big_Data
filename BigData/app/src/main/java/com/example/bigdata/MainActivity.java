package com.example.bigdata;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    EditText et_start_station, et_end_station, et_num_people, et_seat_choice, et_accept_other_seat;
    TextView tv_prompt;
    RadioButton radio_yes, radio_no;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        et_start_station = findViewById(R.id.et_start_station);
        et_end_station = findViewById(R.id.et_end_station);
        et_num_people = findViewById(R.id.et_num_people);
        tv_prompt = findViewById(R.id.tv_prompt);
        radio_yes = findViewById(R.id.radio_yes);
        radio_no = findViewById(R.id.radio_no);

        Button btn_submit = findViewById(R.id.btn_submit);
        btn_submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String startStation = et_start_station.getText().toString();
                String endStation = et_end_station.getText().toString();
                String people = et_num_people.getText().toString();
                String num = et_num_people.getText().toString();
                String seatChoice = et_seat_choice.getText().toString();
                String acceptOtherSeat = et_accept_other_seat.getText().toString();
                String promptValue = "";
                if (radio_yes.isChecked()) {
                    promptValue = "1"; // 當"是"被選中時，將其值設為1
                } else if (radio_no.isChecked()) {
                    promptValue = "2"; // 當"否"被選中時，將其值設為2
                }

                fetchData(startStation, endStation, people, num, seatChoice, acceptOtherSeat, promptValue);
            }
        });
    }
    private void fetchData(String startStation, String endStation, String people, String num, String seatChoice, String acceptOtherSeat, String promptValue) {
        String app_id = "B11002064-0b185a9c-e5b5-4196";
        String app_key = "d2da45c3-9a9e-47f2-9b1d-68885bcc08ee";
        String auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token";
        String url = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatusList?%24%24format=JSON";
        String urlFare = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/ODFare?%24format=JSON";

        // Create a Volley request queue
        RequestQueue queue = Volley.newRequestQueue(this);

        // Authentication request
        StringRequest authRequest = new StringRequest(Request.Method.POST, auth_url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try {
                            JSONObject authJSON = new JSONObject(response);
                            String accessToken = authJSON.getString("access_token");

                            // Make data request with access token
                            JsonObjectRequest dataRequest = new JsonObjectRequest(Request.Method.GET, url, null,
                                    new Response.Listener<JSONObject>() {
                                        @Override
                                        public void onResponse(JSONObject response) {
                                            // Process data response
                                            // ...
                                        }
                                    }, new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    // Handle data request error
                                    // ...
                                }
                            }) {
                                @Override
                                public Map<String, String> getHeaders() {
                                    Map<String, String> headers = new HashMap<>();
                                    headers.put("Authorization", "Bearer " + accessToken);
                                    return headers;
                                }
                            };
                            queue.add(dataRequest);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                // Handle authentication error
                // ...
            }
        });

        // Add the authentication request to the queue
        queue.add(authRequest);
    }
}
