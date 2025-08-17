import React from 'react';
import { Button, ButtonGroup } from '@chakra-ui/react';
import { useLocalization } from '../hooks/useLocalization';

const LanguageSwitcher = () => {
  const { locale, changeLanguage } = useLocalization();

  const handleLanguageChange = (newLocale) => {
    changeLanguage(newLocale);
    // Recargar la página después de un pequeño delay para permitir que se guarde el cambio
    setTimeout(() => {
      window.location.reload();
    }, 100);
  };

  return (
    <ButtonGroup isAttached variant="outline" size="sm">
      <Button
        onClick={() => handleLanguageChange('es')}
        colorScheme={locale === 'es' ? 'blue' : 'gray'}
        variant={locale === 'es' ? 'solid' : 'outline'}
      >
        ES
      </Button>
      <Button
        onClick={() => handleLanguageChange('en')}
        colorScheme={locale === 'en' ? 'blue' : 'gray'}
        variant={locale === 'en' ? 'solid' : 'outline'}
      >
        EN
      </Button>
    </ButtonGroup>
  );
};

export default LanguageSwitcher;
