package com.example.bodymeasurementdisplay.ui.wishlist

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.bodymeasurementdisplay.R
import com.example.bodymeasurementdisplay.ui.wishlist.Model.Wishlist

class GalleryFragment : Fragment() {

    protected lateinit var root: View
    //private var layoutManager: RecyclerView.LayoutManager? = null
    //private var adapter: RecyclerView.Adapter<WishlistAdapter.ViewHolder>? = null

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {
        root = inflater.inflate(R.layout.fragment_gallery, container, false)
        return root
    }

    override fun onViewCreated(itemView: View, savedInstanceState: Bundle?) {
        super.onViewCreated(itemView, savedInstanceState)
        val wishlist = root.findViewById<RecyclerView>(R.id.wishlist)
        val products = arrayListOf<Wishlist>()
        for (i in 0..100){
            products.add(Wishlist("White Tshirt", "", 400.0))
        }
        wishlist.apply{
            layoutManager = LinearLayoutManager(this@GalleryFragment.requireActivity())
            adapter = WishlistAdapter(products)
        }
    }

}