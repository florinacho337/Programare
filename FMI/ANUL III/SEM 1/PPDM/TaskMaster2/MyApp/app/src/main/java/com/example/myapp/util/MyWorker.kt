package com.example.myapp.util

import android.content.Context
import android.util.Log
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.example.myapp.MyApplication

class MyWorker(
    context: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        val appContext = applicationContext as MyApplication
        val taskRepository = appContext.container.taskRepository

        return try {
            taskRepository.syncLocalToRemote()
            Log.d("MyWorker", "Data synchronization completed successfully.")
            Result.success()
        } catch (e: Exception) {
            Log.e("MyWorker", "Data synchronization failed", e)
            Result.retry()
        }
    }
}
