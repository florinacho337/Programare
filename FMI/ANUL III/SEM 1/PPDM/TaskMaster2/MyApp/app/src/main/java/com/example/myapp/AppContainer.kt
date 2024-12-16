package com.example.myapp.core

import android.content.Context
import android.util.Log
import androidx.datastore.preferences.preferencesDataStore
import com.example.myapp.MyAppDatabase
import com.example.myapp.auth.data.AuthRepository
import com.example.myapp.auth.data.remote.AuthDataSource
import com.example.myapp.core.data.UserPreferencesRepository
import com.example.myapp.core.data.remote.Api
import com.example.myapp.todo.data.TaskRepository
import com.example.myapp.todo.data.remote.TaskService
import com.example.myapp.todo.data.remote.TaskWsClient
import com.example.myapp.util.ConnectivityManagerNetworkMonitor

val Context.userPreferencesDataStore by preferencesDataStore(
    name = "user_preferences"
)

class AppContainer(val context: Context) {
    init {
        Log.d(TAG, "init")
    }

    private val taskService: TaskService = Api.retrofit.create(TaskService::class.java)
    private val taskWsClient: TaskWsClient = TaskWsClient(Api.okHttpClient)
    private val authDataSource: AuthDataSource = AuthDataSource()

    private val database: MyAppDatabase by lazy { MyAppDatabase.getDatabase(context) }

    val taskRepository: TaskRepository by lazy {
        TaskRepository(taskService, taskWsClient, database.taskDao())
    }

    val authRepository: AuthRepository by lazy {
        AuthRepository(authDataSource)
    }

    val userPreferencesRepository: UserPreferencesRepository by lazy {
        UserPreferencesRepository(context.userPreferencesDataStore)
    }

    val networkMonitor: ConnectivityManagerNetworkMonitor = ConnectivityManagerNetworkMonitor(context.applicationContext)
}
