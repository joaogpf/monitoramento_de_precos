import React from "react";
import axios from axios
import { useState } from "react";

const Form = () => {

    const [url, setUrl] = useState('')
    

    const handleSubmit = async (e) => {
        e.preventDefault()
        const response = await axios.post("", {
            url
        })
    }
}

export default Form