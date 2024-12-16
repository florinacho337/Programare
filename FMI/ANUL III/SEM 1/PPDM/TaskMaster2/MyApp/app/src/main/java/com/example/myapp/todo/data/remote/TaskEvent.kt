package com.example.myapp.todo.data.remote

import com.example.myapp.todo.data.Task

data class TaskEvent(val type: String, val payload: Task)
