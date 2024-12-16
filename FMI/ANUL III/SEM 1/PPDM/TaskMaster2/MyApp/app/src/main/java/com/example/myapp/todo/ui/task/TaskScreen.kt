package com.example.myapp.todo.ui

import android.util.Log
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.myapp.R
import com.example.myapp.core.Result
import com.example.myapp.todo.ui.task.TaskViewModel
import java.time.Instant
import java.time.LocalDate
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.time.format.DateTimeParseException

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TaskScreen(taskId: String?, onClose: () -> Unit) {
    val taskViewModel = viewModel<TaskViewModel>(factory = TaskViewModel.Factory(taskId))
    val taskUiState = taskViewModel.uiState
    var name by rememberSaveable { mutableStateOf(taskUiState.task.name) }
    var description by rememberSaveable { mutableStateOf(taskUiState.task.description) }
    var progress by rememberSaveable { mutableStateOf(taskUiState.task.progress.toFloat()) }
    var isFinished by rememberSaveable { mutableStateOf(taskUiState.task.finished) }
    var deadlineString by rememberSaveable { mutableStateOf("") }
    var isDeadlineValid by remember { mutableStateOf(true) }

    Log.d("taskScreen", "recompose, name = $name")

    // Handle submission and close screen
    LaunchedEffect(taskUiState.submitResult) {
        Log.d("taskScreen", "Submit = ${taskUiState.submitResult}")
        if (taskUiState.submitResult is Result.Success) {
            Log.d("taskScreen", "Closing screen")
            onClose()
        }
    }

    // Handle loading initial values
    var textInitialized by remember { mutableStateOf(taskId == null) }
    LaunchedEffect(taskId, taskUiState.loadResult) {
        Log.d("taskScreen", "Load result = ${taskUiState.loadResult}")
        if (!textInitialized && taskUiState.loadResult !is Result.Loading) {
            name = taskUiState.task.name
            description = taskUiState.task.description
            progress = taskUiState.task.progress.toFloat()
            isFinished = taskUiState.task.finished
            deadlineString = taskUiState.task.deadline?.let {
                DateTimeFormatter.ofPattern("yyyy-MM-dd")
                    .withZone(ZoneId.systemDefault())
                    .format(it)
            } ?: ""
            textInitialized = true
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(text = stringResource(id = R.string.task)) },
                actions = {
                    Button(onClick = {
                        // Validate the deadline format before saving
                        isDeadlineValid = validateDateFormat(deadlineString)
                        if (isDeadlineValid) {
                            val deadline = deadlineString.takeIf { it.isNotEmpty() }?.let {
                                try {
                                    val localDate = LocalDate.parse(it, DateTimeFormatter.ofPattern("yyyy-MM-dd"))
                                    localDate.atStartOfDay(ZoneId.systemDefault()).plusHours(5).toInstant()
                                } catch (e: DateTimeParseException) {
                                    null // Return null if parsing fails
                                }
                            }
                            taskViewModel.saveOrUpdatetask(
                                name = name,
                                description = description,
                                deadline = deadline,
                                finished = isFinished,
                                progress = progress.toInt()
                            )
                        }
                    }) {
                        Text("Save")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .padding(paddingValues)
                .padding(16.dp)
                .fillMaxSize(),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            if (taskUiState.loadResult is Result.Loading) {
                CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally))
                return@Column
            }

            // Task Name Input
            TextField(
                value = name,
                onValueChange = { name = it },
                label = { Text("Task Name") },
                modifier = Modifier.fillMaxWidth()
            )

            // Task Description Input
            TextField(
                value = description,
                onValueChange = { description = it },
                label = { Text("Description") },
                modifier = Modifier.fillMaxWidth()
            )

            // Progress Slider
            Column {
                Text("Progress: ${progress.toInt()}%", modifier = Modifier.padding(bottom = 8.dp))
                Slider(
                    value = progress,
                    onValueChange = { progress = it },
                    valueRange = 0f..100f,
                    modifier = Modifier.fillMaxWidth()
                )
            }

            // Finished Checkbox
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Finished")
                Checkbox(
                    checked = isFinished,
                    onCheckedChange = { isFinished = it }
                )
            }

            // Deadline Input with Validation
            Column {
                TextField(
                    value = deadlineString,
                    onValueChange = {
                        deadlineString = it
                        isDeadlineValid = validateDateFormat(it)
                    },
                    label = { Text("Deadline (yyyy-MM-dd)") },
                    modifier = Modifier.fillMaxWidth(),
                    isError = !isDeadlineValid
                )
                if (!isDeadlineValid) {
                    Text(
                        text = "Invalid date format. Please use yyyy-MM-dd.",
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodySmall,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }
            }

            // Error Display (if any)
            if (taskUiState.loadResult is Result.Error) {
                Text(
                    text = "Failed to load task: ${(taskUiState.loadResult as Result.Error).exception?.message}",
                    color = MaterialTheme.colorScheme.error
                )
            }
            if (taskUiState.submitResult is Result.Error) {
                Text(
                    text = "Failed to submit task: ${(taskUiState.submitResult as Result.Error).exception?.message}",
                    color = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}

// Function to validate date format
fun validateDateFormat(date: String): Boolean {
    return try {
        DateTimeFormatter.ofPattern("yyyy-MM-dd")
            .withZone(ZoneId.systemDefault())
            .parse(date)
        true
    } catch (e: Exception) {
        false
    }
}

@Preview
@Composable
fun PreviewTaskScreen() {
    TaskScreen(taskId = "0", onClose = {})
}
