import React, { useState } from 'react';

const ControlTagsManager = ({ 
  threatId,
  strideCategory,
  initialTags = [],
  onTagsChange,
  placeholder = "Agregar tags de control (ej: ASVS-V2.1.1)"
}) => {
  const [tags, setTags] = useState(initialTags);
  const [inputValue, setInputValue] = useState('');

  const addTag = (tagValue) => {
    const trimmedTag = tagValue.trim();
    if (!trimmedTag) return;

    if (tags.includes(trimmedTag)) {
      alert("Este tag ya está agregado");
      return;
    }

    const newTags = [...tags, trimmedTag];
    setTags(newTags);
    setInputValue('');
    
    if (onTagsChange) {
      onTagsChange(newTags);
    }
  };

  const removeTag = (tagToRemove) => {
    const newTags = tags.filter(tag => tag !== tagToRemove);
    setTags(newTags);
    if (onTagsChange) {
      onTagsChange(newTags);
    }
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      e.preventDefault();
      addTag(inputValue);
    }
  };

  return (
    <div style={{ margin: '10px 0', padding: '10px', border: '1px solid #e2e8f0', borderRadius: '6px', backgroundColor: '#f7fafc' }}>
      <h4 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#333' }}>🏷️ Tags</h4>
      
      {/* Tags existentes */}
      {tags.length > 0 && (
        <div style={{ marginBottom: '10px' }}>
          {tags.map((tag) => (
            <span 
              key={tag} 
              style={{ 
                backgroundColor: '#3182ce', 
                color: 'white', 
                padding: '4px 8px', 
                margin: '2px', 
                borderRadius: '4px',
                fontSize: '12px',
                display: 'inline-block'
              }}
            >
              {tag}
              <button 
                onClick={() => removeTag(tag)}
                style={{ 
                  marginLeft: '5px', 
                  background: 'none', 
                  border: 'none', 
                  color: 'white', 
                  cursor: 'pointer',
                  fontSize: '14px'
                }}
                title={`Eliminar ${tag}`}
              >
                ×
              </button>
            </span>
          ))}
        </div>
      )}

      {/* Input con botón */}
      <div style={{ display: 'flex', gap: '5px' }}>
        <input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleInputKeyDown}
          placeholder={placeholder}
          style={{ 
            flex: 1, 
            padding: '8px', 
            border: '1px solid #ccc', 
            borderRadius: '4px',
            fontSize: '14px'
          }}
        />
        <button
          onClick={() => inputValue.trim() && addTag(inputValue)}
          disabled={!inputValue.trim()}
          style={{ 
            padding: '8px 12px', 
            backgroundColor: inputValue.trim() ? '#3182ce' : '#ccc', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: inputValue.trim() ? 'pointer' : 'not-allowed',
            fontSize: '14px'
          }}
        >
          + Agregar
        </button>
      </div>

      {/* Información de ayuda */}
      <p style={{ fontSize: '12px', color: '#666', margin: '8px 0 4px 0' }}>
        💡 Escribe un tag de control y presiona Enter (ej: ASVS-V2.1.1)
      </p>
      
      {/* Mostrar información de debug */}
      <p style={{ fontSize: '11px', color: '#999', margin: '4px 0' }}>
        STRIDE: {strideCategory} | Tags: {tags.length}
      </p>
    </div>
  );
};

export default ControlTagsManager;
