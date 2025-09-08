import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

test('renders TZU Security login form', () => {
  render(<App />);
  const titleElement = screen.getByText(/TZU Login/i);
  expect(titleElement).toBeInTheDocument();
});
