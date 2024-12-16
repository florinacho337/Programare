package com.example.myapp.todo.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.example.myapp.todo.data.Task
import kotlinx.coroutines.flow.Flow

@Dao
interface TaskDao {
    @Query("SELECT * FROM Tasks")
    fun getAll(): Flow<List<Task>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(task: Task)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(tasks: List<Task>)

    @Update
    suspend fun update(task: Task): Int

    @Query("DELETE FROM Tasks WHERE _id = :id")
    suspend fun deleteById(id: String): Int

    @Query("DELETE FROM Tasks")
    suspend fun deleteAll()
}
