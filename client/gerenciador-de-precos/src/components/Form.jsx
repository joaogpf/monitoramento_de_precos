import React from "react";
import axios from "axios"
import { useState } from "react";
import './Form.css'

const Form = () => {

    const [url, setUrl] = useState('')
    

    const handleSubmit = async (e) => {
        e.preventDefault()

        try {
            const response = await axios.post("http://127.0.0.1:5000/add_product", 
                { url },
                { headers: { "Content-Type": "application/json" } }
            )
        } catch(error) {
            console.error(error)
        }
       
    }

    return (
        <div className="formContainer">
            <form onSubmit={handleSubmit} className="submitForm">
                <label>Url</label>
                <input placeholder="Insira seu link da Amazon" value={url} type="text" onChange={(e) => setUrl(e.target.value)} required/>
                <button type="submit">Cadastrar</button>
            </form>
        </div>
    )
}

export default Form