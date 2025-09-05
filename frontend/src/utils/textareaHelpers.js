/**
 * Utilities for textarea handling
 */

/**
 * Calculate textarea height based on content
 * @param {string} text - Text content
 * @param {number} width - Textarea width
 * @returns {number} - Calculated height in pixels
 */
export const calculateTextareaHeight = (text, width) => {
  const lineHeight = 20; // line height in px
  const padding = 8; // vertical padding
  const baseHeight = 40; // minimum height
  
  if (!text) return baseHeight;
  
  // Estimate number of lines based on text length and width
  const averageCharsPerLine = Math.floor(width / 8); // approximately 8px per character
  const estimatedLines = Math.ceil(text.length / averageCharsPerLine);
  const newLines = (text.match(/\n/g) || []).length;
  
  const totalLines = Math.max(estimatedLines, newLines + 1);
  const calculatedHeight = Math.max(baseHeight, totalLines * lineHeight + padding * 2);
  
  return Math.min(calculatedHeight, 120); // maximum 120px height
};

/**
 * Auto-resize textarea when user types
 * @param {Event} event - Change event from textarea
 */
export const handleTextareaResize = (event) => {
  const textarea = event.target;
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
};
