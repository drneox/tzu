import { useEffect, useState } from 'react';
import CreatableSelect from 'react-select/creatable';
import { getProjects } from '../services';
import { useLocalization } from '../hooks/useLocalization';

const ProjectCombobox = ({ value, onChange, isDisabled = false }) => {
  const { t } = useLocalization();
  const [options, setOptions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    getProjects()
      .then((res) => {
        if (!cancelled) {
          const opts = res.data.map((p) => ({ value: p.id, label: p.name }));
          setOptions(opts);
        }
      })
      .catch(() => {})
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  const handleChange = (selected) => {
    if (!selected) {
      onChange(null);
    } else if (selected.__isNew__) {
      onChange({ id: null, name: selected.value, isNew: true });
    } else {
      onChange({ id: selected.value, name: selected.label, isNew: false });
    }
  };

  const formatCreateLabel = (inputValue) => {
    const template = t?.projects?.createNew || 'Create "{{name}}"';
    return template.replace('{{name}}', inputValue);
  };

  const currentValue = value
    ? value.isNew
      ? { value: value.name, label: value.name, __isNew__: true }
      : { value: value.id, label: value.name }
    : null;

  return (
    <CreatableSelect
      isClearable
      isDisabled={isDisabled}
      isLoading={isLoading}
      options={options}
      value={currentValue}
      onChange={handleChange}
      formatCreateLabel={formatCreateLabel}
      placeholder={t?.projects?.namePlaceholder || 'Select or create project...'}
      noOptionsMessage={() => t?.projects?.namePlaceholder || 'Type to search...'}
      styles={{
        container: (base) => ({ ...base, width: '100%' }),
        control: (base) => ({
          ...base,
          borderColor: '#CBD5E0',
          borderRadius: '6px',
          minHeight: '40px',
          boxShadow: 'none',
          '&:hover': { borderColor: '#A0AEC0' },
        }),
      }}
    />
  );
};

export default ProjectCombobox;
