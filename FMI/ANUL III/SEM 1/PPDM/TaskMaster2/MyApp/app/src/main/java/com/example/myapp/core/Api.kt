package com.example.myapp.coreimport com.google.gson.GsonBuilderimport okhttp3.OkHttpClientimport retrofit2.Retrofitimport retrofit2.converter.gson.GsonConverterFactoryimport java.time.Instantobject Api {    private val url = "192.168.129.154:3000"//    private val url = "192.168.1.148:3000"//    private val url = "192.168.0.194:3000"    private val httpUrl = "http://$url/"    val wsUrl = "ws://$url/"    private var gson = GsonBuilder()        .registerTypeAdapter(Instant::class.java, InstantTypeAdapter())        .create()    val retrofit = Retrofit.Builder()        .baseUrl(httpUrl)        .addConverterFactory(GsonConverterFactory.create(gson))        .build()    val okHttpClient = OkHttpClient.Builder()        .build()}