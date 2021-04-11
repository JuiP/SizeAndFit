package com.example.bodymeasurementdisplay.ui.measureme

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.bodymeasurementdisplay.R
import com.example.bodymeasurementdisplay.ui.measureme.Model.Measurement

class MeasurementAdapter(private val measurement: ArrayList<Measurement>) : RecyclerView.Adapter<MeasurementAdapter.ViewHolder>() {


    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MeasurementAdapter.ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.measurement_row, parent, false)
        return MeasurementAdapter.ViewHolder(view)
    }

    override fun onBindViewHolder(holder: MeasurementAdapter.ViewHolder, position: Int){
        holder.title.text = measurement[position].title
        holder.measure.text = measurement[position].measure.toString()
    }

    override fun getItemCount() =  measurement.size
    class ViewHolder (itemView: View) : RecyclerView.ViewHolder(itemView) {
        val measure: TextView = itemView.findViewById(R.id.measure)
        val title: TextView = itemView.findViewById(R.id.titleM)
    }
}