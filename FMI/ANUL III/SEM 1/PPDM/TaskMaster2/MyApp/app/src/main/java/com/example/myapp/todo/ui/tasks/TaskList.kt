package com.example.myapp.todo.ui.tasks

import android.app.Application
import android.util.Log
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.Checkbox
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import coil.compose.AsyncImage
import com.example.myapp.sensor.ProximitySensorMonitor
import com.example.myapp.todo.data.Task
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.format.DateTimeParseException
import kotlin.math.roundToInt

typealias OnTaskFn = (id: String?) -> Unit

class ProximitySensorViewModel(application: Application) : AndroidViewModel(application) {
    var uiState by mutableStateOf(false)
        private set

    init {
        viewModelScope.launch {
            ProximitySensorMonitor(getApplication()).isNear.collect {
                uiState = it
            }
        }
    }

    companion object {
        fun Factory(application: Application): ViewModelProvider.Factory = viewModelFactory {
            initializer {
                ProximitySensorViewModel(application)
            }
        }
    }
}

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
            ShakingTaskDetail(task, onTaskClick)
        }
    }
}

@Composable
fun ShakingTaskDetail(
    task: Task,
    onTaskClick: OnTaskFn,
) {
    val proximitySensorViewModel = viewModel<ProximitySensorViewModel>(
        factory = ProximitySensorViewModel.Factory(
            LocalContext.current.applicationContext as Application
        )
    )

    val shakeOffset by rememberInfiniteTransition(label = "").animateFloat(
        initialValue = 0f,
        targetValue = 10f, // Adjust the shake intensity
        animationSpec = infiniteRepeatable(
            animation = tween(200, easing = LinearEasing), // Adjust speed of shake
            repeatMode = RepeatMode.Reverse
        ), label = ""
    )

    val offset = if (proximitySensorViewModel.uiState) shakeOffset else 0f

    Box(
        modifier = Modifier.offset { IntOffset(offset.roundToInt(), 0) }
    ) {
        TaskDetail(task = task, onTaskClick = onTaskClick)
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

    var isExpanded by remember { mutableStateOf(false) }

    Surface(
        modifier = Modifier.fillMaxWidth(),
        onClick = { isExpanded = !isExpanded }
    ) {
        Column(
            modifier = Modifier
                .padding(end = 8.dp)
                .animateContentSize(),
            verticalArrangement = Arrangement.Center
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Column(
                    modifier = Modifier
                        .weight(0.7f)
                ) {
                    Text(
                        text = AnnotatedString(task.name),
                        style = TextStyle(
                            fontSize = 24.sp,
                            color = Color.White
                        )
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
                        progress = { (task.progress.toFloat() / 100).coerceIn(0f, 1f) },
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
            if (isExpanded) {
                Row {
                    Column(
                        modifier = Modifier
                            .weight(0.7f)
                    ) {
                        Text(
                            text = "Description: ${task.description}",
                            style = TextStyle(fontSize = 16.sp)
                        )
                        Text(
                            text = "Deadline: $formattedDeadline",
                            style = TextStyle(fontSize = 16.sp)
                        )

                        task.imageUri?.let { imageUri ->
                            Spacer(modifier = Modifier.height(8.dp)) // Add spacing before the image
                            AsyncImage(
                                model = imageUri,
                                contentDescription = "Task Image",
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(100.dp)
                            )
                        }
                    }

                    Column (
                        modifier = Modifier
                            .weight(0.3f),
                        verticalArrangement = Arrangement.Center
                    ) {
                        androidx.compose.material3.Icon(
                            imageVector = androidx.compose.material.icons.Icons.Default.Edit,
                            contentDescription = "Edit Task",
                            modifier = Modifier
                                .padding(start = 8.dp)
                                .clickable { onTaskClick(task._id) },
                            tint = Color.White
                        )
                    }
                }
            }
        }
    }
}