import { Link, useLocation } from 'react-router-dom';
import { Factory, AlertTriangle, Home } from 'lucide-react';

 export  const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav style={styles.nav}>
      <div style={styles.container}>
        <div style={styles.brand}>
          <Factory size={32} color="#fff" />
          <span style={styles.title}>Sistema Industrial Inteligente</span>
        </div>
        <div style={styles.menu}>
          <Link
            to="/"
            style={{
              ...styles.link,
              ...(isActive('/') ? styles.linkActive : {})
            }}
          >
            <Home size={20} />
            Dashboard
          </Link>
          <Link
            to="/alerts"
            style={{
              ...styles.link,
              ...(isActive('/alerts') ? styles.linkActive : {})
            }}
          >
            <AlertTriangle size={20} />
            Alertas
          </Link>
        </div>
      </div>
    </nav>
  );
};

const styles = {
  nav: {
    background: 'rgba(255, 255, 255, 0.95)',
    backdropFilter: 'blur(10px)',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    position: 'sticky',
    top: 0,
    zIndex: 1000,
  },
  container: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '16px 20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  brand: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  title: {
    fontSize: '20px',
    fontWeight: '700',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
  menu: {
    display: 'flex',
    gap: '20px',
  },
  link: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '8px 16px',
    borderRadius: '8px',
    color: '#333',
    textDecoration: 'none',
    fontWeight: '500',
    transition: 'all 0.3s',
  },
  linkActive: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
  },
};

export default Navbar;