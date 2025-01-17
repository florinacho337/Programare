package com.example.myapp.todo.data

import android.content.Context
import android.util.Log
import androidx.work.Constraints
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.NetworkType
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import com.example.myapp.core.TAG
import com.example.myapp.core.data.remote.Api
import com.example.myapp.todo.data.local.TaskDao
import com.example.myapp.todo.data.remote.TaskEvent
import com.example.myapp.todo.data.remote.TaskService
import com.example.myapp.todo.data.remote.TaskWsClient
import com.example.myapp.util.MyWorker
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.withContext
import java.util.concurrent.TimeUnit

class TaskRepository(
    private val taskService: TaskService,
    private val taskWsClient: TaskWsClient,
    private val taskDao: TaskDao
) {
    val taskStream by lazy { taskDao.getAll() }

    init {
        Log.d(TAG, "init")
    }

    private fun getBearerToken(): String {
        val token = "Bearer ${Api.tokenInterceptor.token}"
        Log.d(TAG, "Bearer Token: $token")
        return token
    }
    suspend fun refresh() {
        Log.d(TAG, "refresh started")
        try {
            val tasks = taskService.find(authorization = getBearerToken())
            taskDao.deleteAll()
            tasks.forEach { task ->
                Log.d(TAG, "Inserting task: $task")
                taskDao.insert(task)
            }
            Log.d(TAG, "refresh succeeded")
        } catch (e: Exception) {
            Log.w(TAG, "refresh failed", e)
        }
    }

    suspend fun openWsClient() {
        Log.d(TAG, "openWsClient")
        withContext(Dispatchers.IO) {
            getTaskEvents().collect {
                Log.d(TAG, "Task event collected $it")
                if (it.isSuccess) {
                    val taskEvent = it.getOrNull();
                    when (taskEvent?.type) {
                        "created" -> saveTaskLocally(taskEvent.payload)
                        "updated" -> updateTaskLocally(taskEvent.payload)
                        "deleted" -> handleTaskDeleted(taskEvent.payload)
                    }
                }
            }
        }
    }

    suspend fun closeWsClient() {
        Log.d(TAG, "closeWsClient")
        withContext(Dispatchers.IO) {
            taskWsClient.closeSocket()
        }
    }

    suspend fun getTaskEvents(): Flow<kotlin.Result<TaskEvent>> = callbackFlow {
        Log.d(TAG, "getTaskEvents started")
        taskWsClient.openSocket(
            onEvent = {
                Log.d(TAG, "onEvent $it")
                if (it != null) {
                    trySend(kotlin.Result.success(it))
                }
            },
            onClosed = { close() },
            onFailure = { close() });
        awaitClose { taskWsClient.closeSocket() }
    }

    suspend fun update(task: Task): Task {
        Log.d(TAG, "update $task...")
        val updatedTask =
            taskService.update(taskId = task._id, task = task, authorization = getBearerToken())
        Log.d(TAG, "update $task succeeded")
        updateTaskLocally(updatedTask)
        return updatedTask
    }

    suspend fun save(task: Task): Task {
        Log.d(TAG, "save $task...")
        val createdTask = taskService.create(task = task, authorization = getBearerToken())
        Log.d(TAG, "save $task succeeded")
        saveTaskLocally(createdTask)
        return createdTask
    }

    private suspend fun handleTaskDeleted(task: Task) {
        Log.d(TAG, "handleTaskDeleted - todo $task")
    }

    suspend fun updateTaskLocally(task: Task) {
        Log.d(TAG, "handleTaskUpdated...")
        taskDao.update(task)
    }

    suspend fun saveTaskLocally(task: Task) {
        Log.d(TAG, "handleTaskCreated...")
        taskDao.insert(task)
    }

    suspend fun deleteAll() {
        taskDao.deleteAll()
    }

    fun setToken(token: String) {
        taskWsClient.authorize(token)
    }

    suspend fun syncLocalToRemote() {
        Log.d(TAG, "syncLocalToRemote started")
        try {
            // Fetch all tasks from the local database
            val localTasks = taskDao.getAll()

            // Iterate over local tasks and push changes to the remote server
            localTasks.first().forEach { task ->
                if (task.isNew) {
                    // Create new task on remote server
                    taskService.create(task = task, authorization = getBearerToken())
                    task.isNew = false // Mark as synced
                    taskDao.update(task) // Update local DB
                    Log.d(TAG, "Created new task on remote: $task")
                } else if (task.isUpdated) {
                    // Update task on remote server
                    task.isUpdated = false // Mark as synced
                    taskService.update(
                        taskId = task._id,
                        task = task,
                        authorization = getBearerToken()
                    )
                    taskDao.update(task) // Update local DB
                    Log.d(TAG, "Updated task on remote: $task")
                }
            }
            Log.d(TAG, "syncLocalToRemote completed successfully")
        } catch (e: Exception) {
            Log.w(TAG, "Error syncing local to remote", e)
        }
    }
}