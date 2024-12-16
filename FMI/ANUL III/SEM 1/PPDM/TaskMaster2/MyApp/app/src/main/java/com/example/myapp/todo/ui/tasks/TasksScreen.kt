package com.example.myapp.todo.ui.tasks

import android.util.Log
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.myapp.R

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TasksScreen(onTaskClick: (id: String?) -> Unit, onAddTask: () -> Unit, onLogout: () -> Unit) {
    Log.d("TasksScreen", "recompose")
    val tasksViewModel = viewModel<TasksViewModel>(factory = TasksViewModel.Factory)
    val tasksUiState by tasksViewModel.uiState.collectAsStateWithLifecycle(
        initialValue = listOf()
    )
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(text = stringResource(id = R.string.tasks)) },
                actions = {
                    Button(onClick = onLogout) { Text("Logout") }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = {
                    Log.d("TasksScreen", "add")
                    onAddTask()
                },
            ) { Icon(Icons.Rounded.Add, "Add") }
        }
    ) {
        if (tasksUiState.isEmpty()) {
            Text(text = "Loading tasks...")
        } else {
            TaskList(
                taskList = tasksUiState,
                onTaskClick = onTaskClick,
                modifier = Modifier.padding(it)
            )
        }
    }
}

@Preview
@Composable
fun PreviewTasksScreen() {
    TasksScreen(onTaskClick = {}, onAddTask = {}, onLogout = {})
}
