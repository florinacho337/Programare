package com.example.myapp.todo.ui.task

import android.content.Context
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.myapp.MyApplication
import com.example.myapp.core.Result
import com.example.myapp.core.TAG
import com.example.myapp.todo.data.Task
import com.example.myapp.todo.data.TaskRepository
import com.example.myapp.util.ConnectivityManagerNetworkMonitor
import com.example.myapp.util.showSimpleNotification
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import java.time.Instant

data class taskUiState(
    val taskId: String? = null,
    val task: Task = Task(),
    var loadResult: Result<Task>? = null,
    var submitResult: Result<Task>? = null,
)

class TaskViewModel(
    private val taskId: String?,
    private val taskRepository: TaskRepository,
    private val networkMonitor: ConnectivityManagerNetworkMonitor,
    private val context: Context
) :
    ViewModel() {

    var uiState: taskUiState by mutableStateOf(taskUiState(loadResult = Result.Loading))
        private set

    init {
        Log.d(TAG, "init")
        if (taskId != null) {
            loadTask()
        } else {
            uiState = uiState.copy(loadResult = Result.Success(Task()))
        }
    }

    fun loadTask() {
        viewModelScope.launch {
            taskRepository.taskStream.collect { tasks ->
                if (!(uiState.loadResult is Result.Loading)) {
                    return@collect
                }
                val task = tasks.find { it._id == taskId } ?: Task()
                uiState = uiState.copy(task = task, loadResult = Result.Success(task))
            }
        }
    }


    fun saveOrUpdatetask(
        name: String,
        description: String,
        deadline: Instant?,
        finished: Boolean,
        progress: Int,
        imageUri: String?
    ) {
        viewModelScope.launch {
            Log.d(TAG, "saveOrUpdatetask...");
            Log.d(TAG, "task id: $taskId")

            val task = uiState.task.copy(
                name = name,
                description = description,
                deadline = deadline,
                finished = finished,
                progress = progress,
                imageUri = imageUri
            )

            try {
                if (networkMonitor.isOnline.first()) {
                    uiState = uiState.copy(submitResult = Result.Loading)

                    val savedTask: Task
                    savedTask = if (taskId == null) {
                        taskRepository.save(task)
                    } else {
                        taskRepository.update(task)
                    }

                    Log.d(TAG, "saveOrUpdatetask succeeeded");
                    uiState = uiState.copy(submitResult = Result.Success(savedTask))
                } else {
                    if (taskId == null) {
                        task.isNew = true;
                        taskRepository.saveTaskLocally(task)
                    } else {
                        task.isUpdated = true;
                        taskRepository.updateTaskLocally(task)
                    }
                    showOfflineNotification()
                    uiState = uiState.copy(submitResult = Result.Success(task))
                }
            } catch (e: Exception) {
                Log.d(TAG, "saveOrUpdatetask failed");
                uiState = uiState.copy(submitResult = Result.Error(e))
            }
        }
    }

    private fun showOfflineNotification() {
        showSimpleNotification(
            context = context,
            channelId = "task_offline",
            notificationId = 1,
            textTitle = "Offline Mode",
            textContent = "Task saved locally. Changes will sync once online."
        )
    }

    companion object {
        fun Factory(taskId: String?): ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app =
                    (this[ViewModelProvider.AndroidViewModelFactory.APPLICATION_KEY] as MyApplication)
                TaskViewModel(
                    taskId,
                    app.container.taskRepository,
                    app.container.networkMonitor,
                    app.applicationContext
                    )
            }
        }
    }
}
