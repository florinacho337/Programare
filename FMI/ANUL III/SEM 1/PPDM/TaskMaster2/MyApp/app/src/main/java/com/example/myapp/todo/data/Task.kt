package com.example.myapp.todo.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.time.Instant

@Entity(tableName = "tasks")
data class Task(
    @PrimaryKey val _id: String = "",
    val name: String = "",
    val description:  String = "",
    val deadline: Instant? = Instant.EPOCH,
    val finished: Boolean = false,
    val progress: Int = 0
) {
    var isUpdated: Boolean = false
    var isNew: Boolean = false
}
