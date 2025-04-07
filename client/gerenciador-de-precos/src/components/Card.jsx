import React from "react";
import axios from "axios"
import './Card.css'


import { useState, useEffect } from "react";

const Card = () => {

    const [products, setProducts] = useState([])
    const [prices, setPrices] = useState([])
    

    useEffect (() => {

        const getProducts = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/products")
                const responsePrices = await axios.get("http://127.0.0.1:5000/prices")
                setProducts(response.data)
                setPrices(responsePrices.data)
            } catch(error) {
                console.error(error)
            }
        }
      
        getProducts()
    }, [products, prices])

    return (
        <div className="cardsContainer">
            {products.map((product) => (
                <div className="produto" key={product.id}> 
                    <div className="nome">{product.name}</div>
                    <div className="preco-antigo">R$ {prices[(product.id-1)].old_price}</div>
                    <div className="preco-atual">R$ {prices[(product.id-1)].new_price}</div>
                </div>
            ))}
            
        </div>
    )
}

export default Card