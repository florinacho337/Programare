package com.example.myapp.todo.data.remote

import com.example.myapp.todo.data.Task
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Headers
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path

interface TaskService {
    @GET("/api/task")
    suspend fun find(@Header("Authorization") authorization: String): List<Task>

    @GET("/api/task/{id}")
    suspend fun read(
        @Header("Authorization") authorization: String,
        @Path("id") taskId: String?
    ): Task;

    @Headers("Content-Type: application/json")
    @POST("/api/task")
    suspend fun create(@Header("Authorization") authorization: String, @Body task: Task): Task

    @Headers("Content-Type: application/json")
    @PUT("/api/task/{id}")
    suspend fun update(
        @Header("Authorization") authorization: String,
        @Path("id") taskId: String?,
        @Body task: Task
    ): Task
}
