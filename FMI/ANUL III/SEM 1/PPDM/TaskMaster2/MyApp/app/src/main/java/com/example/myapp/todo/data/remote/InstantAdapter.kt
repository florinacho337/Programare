package com.example.myapp.todo.data.remote
import com.squareup.moshi.FromJson
import com.squareup.moshi.ToJson
import java.time.Instant

class InstantAdapter {
    @ToJson
    fun toJson(instant: Instant): String {
        return instant.toString() // Serialize Instant to ISO-8601 string
    }

    @FromJson
    fun fromJson(value: String): Instant {
        return Instant.parse(value) // Deserialize ISO-8601 string to Instant
    }
}
