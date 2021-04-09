package com.example.bodymeasurementdisplay.ui.wishlist

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.bodymeasurementdisplay.R
import com.example.bodymeasurementdisplay.ui.wishlist.Model.Wishlist

class WishlistAdapter(private val wishlist: ArrayList<Wishlist>) : RecyclerView.Adapter<WishlistAdapter.ViewHolder>() {


    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.wishlist_row, parent, false)
        return ViewHolder(view)
    }

    override fun getItemCount() = wishlist.size

    override fun onBindViewHolder(holder: ViewHolder, position: Int){
        holder.title.text = wishlist[position].title
    }

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val image: ImageView = itemView.findViewById(R.id.photo)
        val title: TextView = itemView.findViewById(R.id.title)
    }
}