package com.example.myapp.todo.data

import androidx.room.TypeConverter
import java.time.Instant

class Converters {
    @TypeConverter
    fun fromIsoString(value: String?): Instant? {
        return value?.let { Instant.parse(it) }
    }

    @TypeConverter
    fun instantToIsoString(instant: Instant?): String? {
        return instant?.toString()
    }
}
