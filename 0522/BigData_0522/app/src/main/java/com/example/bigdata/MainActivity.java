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

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    EditText etStartStation, etEndStation, etNumPeople;
    RadioButton radioYes, radioNo, radioStandardSeat, radioBusinessSeat, radioFreeSeat, radioAccept, radioNotAccept;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 找到並關聯 EditText
        etStartStation = findViewById(R.id.et_start_station);
        etEndStation = findViewById(R.id.et_end_station);
        etNumPeople = findViewById(R.id.et_num_people);

        // 找到並關聯 RadioButton
        radioYes = findViewById(R.id.radio_yes);
        radioNo = findViewById(R.id.radio_no);
        radioStandardSeat = findViewById(R.id.radio_standard_seat);
        radioBusinessSeat = findViewById(R.id.radio_business_seat);
        radioFreeSeat = findViewById(R.id.radio_free_seat);
        radioAccept = findViewById(R.id.radio_accept);
        radioNotAccept = findViewById(R.id.radio_not_accept);

        // 找到並設置按鈕點擊事件
        Button btnSubmit = findViewById(R.id.btn_submit);
        btnSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // 在這裡獲取 EditText 和 RadioButton 的值並執行相應的操作
                String startStation = etStartStation.getText().toString();
                String endStation = etEndStation.getText().toString();
                String numPeople = etNumPeople.getText().toString();

                // 獲取 RadioButton 的選擇
                String promptValue = "";
                if (radioYes.isChecked()) {
                    promptValue = "1"; // 是
                } else if (radioNo.isChecked()) {
                    promptValue = "2"; // 否
                }

                // 在這裡執行後續操作，例如調用 fetchData 方法
                fetchData(startStation, endStation, numPeople, promptValue);
            }
        });
    }
    private void fetchData(String startStation, String endStation, String people, String num, String seatChoice, String acceptOtherSeat, String promptValue) {
        String app_id = "B11002064-0b185a9c-e5b5-4196";
        String app_key = "d2da45c3-9a9e-47f2-9b1d-68885bcc08ee";
        String auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token";
        String url = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatusList?%24%24format=JSON";
        String urlFare = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/ODFare?%24format=JSON";

        String realstation = startStation;
        String endstation = endStation;
        String seat_choice = promptValue;
        String accept_other_seat = "1";

        RequestQueue queue = Volley.newRequestQueue(this);

        List<String[]> trainSeat; // Assuming this is defined elsewhere
        String peopleStatus; // Assuming this is defined elsewhere
        int numPassengers; // Assuming this is defined elsewhere


        StringRequest authRequest = new StringRequest(Request.Method.POST, auth_url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try {
                            JSONObject authJSON = new JSONObject(response);
                            String accessToken = authJSON.getString("access_token");

                            JsonObjectRequest dataRequest = new JsonObjectRequest(Request.Method.GET, url, null,
                                    new Response.Listener<JSONObject>() {
                                        @Override
                                        public void onResponse(JSONObject response) {
                                            try {
                                                // 解析 JSON 回應
                                                JSONArray availableSeats = response.getJSONArray("AvailableSeats");
                                                JSONObject fareData = response.getJSONObject("FareData");
                                                // 處理列車座位狀態
                                                processAvailableSeats(availableSeats);
                                                // 處理票價資訊
                                                processFareData(fareData);
                                            } catch (JSONException e) {
                                                e.printStackTrace();
                                                // 處理 JSON 解析錯誤
                                            }
                                        }
                                        //座位還有部分沒連結
                                        private void processAvailableSeats(JSONArray availableSeats) {
                                            HashSet<String> allTrain = new HashSet<>();

                                            for (int i = 0; i < availableSeats.length(); i++) {
                                                JSONObject seat = availableSeats.getJSONObject(i);
                                                int flag1 = 0;
                                                int flag2 = 0;
                                                JSONArray stopStations = seat.getJSONArray("StopStations");
                                                for (int j = 0; j < stopStations.length(); j++) {
                                                    JSONObject station = stopStations.getJSONObject(j);
                                                    if (station.getJSONObject("StationName").getString("Zh_tw").equals(realstation)) {
                                                        flag1 = 1;
                                                    }
                                                    if (station.getJSONObject("StationName").getString("Zh_tw").equals(endstation) && flag1 == 1) {
                                                        flag2 = 1;
                                                    }
                                                }
                                                if (flag1 == 1 && flag2 == 1) {
                                                    allTrain.add(seat.getString("TrainNo"));
                                                }
                                            }

                                            for (String trainNo : allTrain) {
                                                String station = realstation;
                                                ArrayList<String[]> trainSeat = new ArrayList<>();
                                                JSONObject keep = new JSONObject();
                                                HashMap<String, Integer> trainID = new HashMap<>();

                                                for (int i = 0; i < availableSeats.length(); i++) {
                                                    JSONObject seat = availableSeats.getJSONObject(i);
                                                    if (seat.getString("TrainNo").equals(trainNo)) {
                                                        keep = seat;
                                                        String state = seat.getJSONObject("EndingStationName").getString("Zh_tw");
                                                        JSONArray stopStations = seat.getJSONArray("StopStations");
                                                        for (int j = 0; j < stopStations.length(); j++) {
                                                            JSONObject stationInfo = stopStations.getJSONObject(j);
                                                            trainID.put(stationInfo.getJSONObject("StationName").getString("Zh_tw"), stationInfo.getInt("StopSequence"));
                                                            if (stationInfo.getJSONObject("StationName").getString("Zh_tw").equals(state)) {
                                                                int num = stationInfo.getInt("StopSequence");
                                                                trainID.put(keep.getJSONObject("StationName").getString("Zh_tw"), 1);
                                                            }
                                                        }
                                                    }
                                                }
                                                String canseat = "";
                                                boolean temp = false;
                                                int flag = trainID.get(endstation);

                                                if (seat_choice.equals("1")) {
                                                    for (int i = 0; i < keep.getJSONArray("StopStations").length(); i++) {
                                                        JSONObject stationInfo = keep.getJSONArray("StopStations").getJSONObject(i);
                                                        if (stationInfo.getJSONObject("StationName").getString("Zh_tw").equals(start_station)) {
                                                            continue;
                                                        }
                                                        if (stationInfo.getInt("StopSequence") > flag) {
                                                            continue;
                                                        }
                                                        if (stationInfo.getString("StandardSeatStatus").equals("O") || stationInfo.getString("StandardSeatStatus").equals("L")) {
                                                            if (stationInfo.getInt("StopSequence") >= trainID.get(start_station)) {
                                                                canseat = stationInfo.getJSONObject("StationName").getString("Zh_tw");
                                                                temp = true;
                                                            }
                                                        } else {
                                                            break;
                                                        }
                                                    }
                                                    if (temp) {
                                                        trainSeat.add(new String[]{start_station, canseat, "1"});
                                                    }
                                                    station = canseat;
                                                    String scanseat = canseat;

                                                    if (!station.equals(end_station)) {
                                                        if (accept_other_seat.equals("1")) {
                                                            while (!station.equals(end_station)) {
                                                                temp = false;
                                                                station = canseat;
                                                                JSONObject data = new JSONObject(data_response);
                                                                keep = new JSONObject();
                                                                JSONArray availableSeatsArray = data.getJSONArray("AvailableSeats");
                                                                for (int i = 0; i < availableSeatsArray.length(); i++) {
                                                                    JSONObject seatInfo = availableSeatsArray.getJSONObject(i);
                                                                    if (seatInfo.getString("TrainNo").equals("1514")) {
                                                                        JSONArray stopStations = seatInfo.getJSONArray("StopStations");
                                                                        for (int j = 0; j < stopStations.length(); j++) {
                                                                            JSONObject stationInfo = stopStations.getJSONObject(j);
                                                                            if (stationInfo.getInt("StopSequence") <= trainID.get(station) || stationInfo.getInt("StopSequence") > trainID.get(end_station)) {
                                                                                continue;
                                                                            }
                                                                            keep.put(String.valueOf(stationInfo.getInt("StopSequence")), stationInfo);
                                                                        }
                                                                    }
                                                                }
                                                                int count = trainID.get(station) + 1;
                                                                for (String key : keep.keySet()) {
                                                                    JSONObject stationInfo = keep.getJSONObject(key);
                                                                    if (stationInfo.getString("BusinessSeatStatus").equals("O") || stationInfo.getString("BusinessSeatStatus").equals("L")) {
                                                                        canseat = stationInfo.getJSONObject("StationName").getString("Zh_tw");
                                                                        scanseat = stationInfo.getJSONObject("StationName").getString("Zh_tw");
                                                                        temp = true;
                                                                    } else {
                                                                        break;
                                                                    }
                                                                    count++;
                                                                }
                                                                if (temp) {
                                                                    trainSeat.add(new String[]{station, canseat, "2"});
                                                                } else {
                                                                    if (keep.has(String.valueOf(trainID.get(station) + 1))) {
                                                                        canseat = keep.getJSONObject(String.valueOf(trainID.get(station) + 1)).getJSONObject("StationName").getString("Zh_tw");
                                                                        station = canseat;
                                                                    }
                                                                }
                                                            }//
                                                        }
                                                    }
                                                } else if (seat_choice.equals("2")) {
                                                    for (int i = 0; i < keep.getJSONArray("StopStations").length(); i++) {
                                                        JSONObject stationInfo = keep.getJSONArray("StopStations").getJSONObject(i);
                                                        if (stationInfo.getInt("StopSequence") > trainID.get(end_station)) {
                                                            continue;
                                                        }
                                                        if (stationInfo.getString("BusinessSeatStatus").equals("O") || stationInfo.getString("BusinessSeatStatus").equals("L")) {
                                                            if (stationInfo.getInt("StopSequence") >= trainID.get(start_station)) {
                                                                canseat = stationInfo.getJSONObject("StationName").getString("Zh_tw");
                                                                temp = true;
                                                            }
                                                        } else {
                                                            break;
                                                        }
                                                    }
                                                    if (temp) {
                                                        trainSeat.add(new String[]{start_station, canseat, "2"});
                                                    }
                                                    station = canseat;
                                                    String scanseat = canseat;

                                                    if (!station.equals(end_station)) {
                                                        if (accept_other_seat.equals("1")) {
                                                            while (!station.equals(end_station)) {
                                                                temp = false;
                                                                station = canseat;
                                                                JSONObject data = new JSONObject(data_response);
                                                                keep = new JSONObject();
                                                                JSONArray availableSeatsArray = data.getJSONArray("AvailableSeats");
                                                                for (int i = 0; i < availableSeatsArray.length(); i++) {
                                                                    JSONObject seatInfo = availableSeatsArray.getJSONObject(i);
                                                                    if (seatInfo.getString("TrainNo").equals("1514")) {
                                                                        JSONArray stopStations = seatInfo.getJSONArray("StopStations");
                                                                        for (int j = 0; j < stopStations.length(); j++) {
                                                                            JSONObject stationInfo = stopStations.getJSONObject(j);
                                                                            if (stationInfo.getInt("StopSequence") <= trainID.get(station) || stationInfo.getInt("StopSequence") > trainID.get(end_station)) {
                                                                                continue;
                                                                            }
                                                                            keep.put(String.valueOf(stationInfo.getInt("StopSequence")), stationInfo);
                                                                        }
                                                                    }
                                                                }
                                                                int count = trainID.get(station) + 1;
                                                                for (String key : keep.keySet()) {
                                                                    JSONObject stationInfo = keep.getJSONObject(key);
                                                                    if (stationInfo.getString("StandardSeatStatus").equals("O") || stationInfo.getString("StandardSeatStatus").equals("L")) {
                                                                        canseat = stationInfo.getJSONObject("StationName").getString("Zh_tw");
                                                                        scanseat = stationInfo.getJSONObject("StationName").getString("Zh_tw");
                                                                        temp = true;
                                                                    } else {
                                                                        break;
                                                                    }
                                                                    count++;
                                                                }
                                                                if (temp) {
                                                                    trainSeat.add(new String[]{station, canseat, "1"});
                                                                } else {
                                                                    if (keep.has(String.valueOf(trainID.get(station) + 1))) {
                                                                        canseat = keep.getJSONObject(String.valueOf(trainID.get(station) + 1)).getJSONObject("StationName").getString("Zh_tw");
                                                                        station = canseat;
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                        //處理票價 還有Map沒處理
                                        private void processFareData(JSONObject fareData) {
                                            try {
                                                JSONArray data = fareData.getJSONArray("Fares");

                                                Map<String, Integer> allFares = new HashMap<>();
                                                for (int i = 0; i < data.length(); i++) {
                                                    JSONObject fare = data.getJSONObject(i);
                                                    String ticketType = fare.getString("TicketType");
                                                    String fareClass = fare.getString("FareClass");
                                                    String cabinClass = fare.getString("CabinClass");
                                                    int price = fare.getInt("Price");
                                                    String key = ticketType + fareClass + cabinClass;
                                                    allFares.put(key, price);
                                                }
                                                for (String[] seat : trainSeat) {
                                                    String start = seat[0];
                                                    String end = seat[1];
                                                    String name = start + "_" + end;
                                                    List<String> ticket = new ArrayList<>();
                                                    if (seat[2].equals("1")) {
                                                        ticket.add("111");
                                                        if (numPassengers >= 11) {
                                                            ticket.add("811");
                                                        }
                                                        if (peopleStatus.equals("1")) {
                                                            ticket.add("191");
                                                        }
                                                    } else if (seat[2].equals("2")) {
                                                        ticket.add("112");
                                                        if (numPassengers >= 11) {
                                                            ticket.add("812");
                                                        }
                                                        if (peopleStatus.equals("1")) {
                                                            ticket.add("192");
                                                        }
                                                    }
                                                    int price = 10000;
                                                    String endTicket = "";
                                                    for (String t : ticket) {
                                                        if (allFares.containsKey(name + t) && allFares.get(name + t) < price) {
                                                            endTicket = t;
                                                            price = allFares.get(name + t);
                                                        }
                                                    }
                                                    if (seat[2].equals("1")) {
                                                        resultText.append("坐標準座從" + start + "坐到" + end + "要" + price + "元\n");
                                                    } else if (seat[2].equals("2")) {
                                                        resultText.append("坐商務坐從" + start + "坐到" + end + "要" + price + "元\n");
                                                    }
                                                }

                                                if (seatChoice.equals("3")) {
                                                    String name = startStation + "_" + endStation;
                                                    List<String> ticket = new ArrayList<>();
                                                    ticket.add("113");
                                                    if (peopleStatus.equals("1")) {
                                                        ticket.add("193");
                                                    }
                                                    int price = 10000;
                                                    String endTicket = "";
                                                    for (String t : ticket) {
                                                        if (allFares.containsKey(name + t) && allFares.get(name + t) < price) {
                                                            endTicket = t;
                                                            price = allFares.get(name + t);
                                                        }
                                                    }
                                                    resultText.append("坐自由座從 " + startStation + " 到 " + endStation + " 要 " + price + " 元\n");
                                                }

                                            } catch (JSONException e) {
                                                e.printStackTrace();
                                            }
                                        }

                                    }, new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    // 處理請求錯誤
                                    // 顯示錯誤消息給用戶
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

            }
        });
        queue.add(authRequest);
    }

}
