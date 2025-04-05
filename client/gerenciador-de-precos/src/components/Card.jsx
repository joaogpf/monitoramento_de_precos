import React from "react";
import axios from "axios"
import './Card.css'

import { useState, useEffect } from "react";

const Card = () => {

    const [products, setProducts] = useState([])
    

    useEffect (() => {

        const getProducts = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/products")
                setProducts(response.data)
            } catch(error) {
                console.error(error)
            }
        }
      
        getProducts()
    }, [products])

    return (
        <div className="cardsContainer">
            {products.map((product) => (
                <div className="produto" key={product.id}> 
                    <div className="nome">{product.name}</div>
                    <div className="preco">{product.price}</div>
                </div>
            ))}
            
        </div>
    )
}

export default Card