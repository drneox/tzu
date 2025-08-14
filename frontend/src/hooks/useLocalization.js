import { useState, useEffect } from 'react';
import enTranslations from '../locales/en.json';
import esTranslations from '../locales/es.json';

const translations = {
  en: enTranslations,
  es: esTranslations
};

export const useLocalization = () => {
  const [locale, setLocale] = useState('en'); // English by default
  const [t, setT] = useState(translations.en);

  useEffect(() => {
    setT(translations[locale] || translations.en);
  }, [locale]);

  const changeLanguage = (newLocale) => {
    if (translations[newLocale]) {
      setLocale(newLocale);
      localStorage.setItem('tzu-locale', newLocale);
    }
  };

  useEffect(() => {
    const savedLocale = localStorage.getItem('tzu-locale');
    if (savedLocale && translations[savedLocale]) {
      setLocale(savedLocale);
    }
  }, []);

  return {
    locale,
    t,
    changeLanguage,
    translations: translations[locale]
  };
};

// Función helper para obtener valores OWASP localizados
export const getOwaspValues = (locale = 'es') => {
  const trans = translations[locale] || translations.es;
  return trans.owasp;
};

// Función helper para crear opciones de select
export const getOwaspSelectOptions = (factorName, locale = 'es') => {
  const trans = translations[locale] || translations.es;
  const values = trans.owasp.values[factorName] || {};
  
  // Solo incluir valores que tienen descripción definida
  return Object.keys(values)
    .map(key => parseInt(key))
    .filter(value => !isNaN(value))
    .sort((a, b) => a - b)
    .map(value => ({
      value: value,
      label: `${value} - ${values[value.toString()]}`
    }));
};
