import React, { useState } from 'react';
import axios from 'axios';
import './queryform.css';

const QueryForm = () => {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleQueryChange = (event) => {
        setQuery(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!query) {
            setError("Please enter a query.");
            return;
        }

        setLoading(true);
        setError('');
        try {
            const res = await axios.post('http://localhost:5000/query', { query });
            setResponse(res.data.response);
        } catch (err) {
            setError("Error processing your request.");
            console.error("API call error:", err.response || err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="query-container">
            <div className="query-box">
                <h2 className="query-heading">How can I help you today?</h2>
               
                <form onSubmit={handleSubmit} className="query-form">
                    <textarea
                        value={query}
                        onChange={handleQueryChange}
                        placeholder="Type your prompt here..."
                        rows="3"
                        className="query-input"
                    />
                    <button type="submit" disabled={loading} className="query-submit">
                        {loading ? <span className="spinner"></span> : '→'}
                    </button>
                </form>

                <p className="query-description">This AI Application will help you find sources to write your research paper , after asking the question please include to list papers for reference.</p>
                {error && <div className="query-error">{error}</div>}
                {response && <div className="query-response">{response}</div>}
            </div>
        </div>
    );
};

export default QueryForm;
