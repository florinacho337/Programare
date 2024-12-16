package com.example.myapp.todo.ui.tasks

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.myapp.MyApplication
import com.example.myapp.core.TAG
import com.example.myapp.todo.data.Task
import com.example.myapp.todo.data.TaskRepository
import com.example.myapp.util.ConnectivityManagerNetworkMonitor
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.launch

class TasksViewModel(private val taskRepository: TaskRepository) : ViewModel() {
    val uiState: Flow<List<Task>> = taskRepository.taskStream

    init {
        Log.d(TAG, "init")
        loadTasks()
        observeNetworkConnectivity()
    }

    fun loadTasks() {
        Log.d(TAG, "loadTasks...")
        viewModelScope.launch {
            taskRepository.refresh()
        }
    }

    private fun observeNetworkConnectivity() {
        val networkMonitor = ConnectivityManagerNetworkMonitor(MyApplication.appContext)

        viewModelScope.launch {
            networkMonitor.isOnline.collect { isOnline ->
                if (isOnline) {
                    Log.d(TAG, "Network is back, syncing data...")
                    taskRepository.syncLocalToRemote()
                } else {
                    Log.d(TAG, "Network lost, sync will retry when online.")
                }
            }
        }
    }

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app =
                    (this[ViewModelProvider.AndroidViewModelFactory.APPLICATION_KEY] as MyApplication)
                TasksViewModel(app.container.taskRepository)
            }
        }
    }
}
