package com.example.myapp.todo.ui.tasks

import android.util.Log
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.ClickableText
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.myapp.todo.data.Task
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Checkbox
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.Color
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.myapp.auth.TAG
import com.example.myapp.todo.ui.task.TaskViewModel
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.format.DateTimeParseException

typealias OnTaskFn = (id: String?) -> Unit

@Composable
fun TaskList(
    taskList: List<Task>,
    onTaskClick: OnTaskFn,
    modifier: Modifier
) {
    Log.d("taskList", "recompose")
    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(12.dp)
    ) {
        items(taskList) { task ->
            TaskDetail(task, onTaskClick)
        }
    }
}

@Composable
fun TaskDetail(
    task: Task,
    onTaskClick: OnTaskFn,
) {
    val formattedDeadline = try {
        val inputFormatter = DateTimeFormatter.ISO_OFFSET_DATE_TIME
        val outputFormatter = DateTimeFormatter.ofPattern("dd-MM-yyyy")
        LocalDate.parse(task.deadline.toString(), inputFormatter).format(outputFormatter)
    } catch (e: DateTimeParseException) {
        "Invalid date"
    }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Column(
            modifier = Modifier
                .weight(1f)
                .padding(end = 8.dp),
            verticalArrangement = Arrangement.Center
        ) {
            ClickableText(
                text = AnnotatedString(task.name),
                style = TextStyle(
                    fontSize = 24.sp,
                    color = Color.White
                ),
                onClick = { onTaskClick(task._id) }
            )
            Text(
                text = "Description: ${task.description}",
                style = TextStyle(fontSize = 16.sp)
            )
            Text(
                text = "Deadline: $formattedDeadline",
                style = TextStyle(fontSize = 16.sp)
            )
        }

        Column(
            modifier = Modifier
                .padding(start = 8.dp)
                .weight(0.3f),
            verticalArrangement = Arrangement.Center
        ) {
            Checkbox(
                checked = task.finished,
                onCheckedChange = null
            )
            Spacer(modifier = Modifier.height(8.dp))

            // Progress Bar for "progress"
            LinearProgressIndicator(
                progress = (task.progress.toFloat() / 100).coerceIn(0f, 1f),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(end = 4.dp),
            )
            Text(
                text = "${task.progress}%",
                style = TextStyle(fontSize = 14.sp)
            )
        }
    }
}