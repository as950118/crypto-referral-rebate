import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import { 
  Wallet, 
  Settings, 
  Copy, 
  CheckCircle, 
  AlertCircle,
  ExternalLink,
  Plus,
  Eye,
  EyeOff
} from 'lucide-react';
import { AppDispatch, RootState } from '../store';
import { fetchExchanges, configureExchangeAPI } from '../store/slices/exchangeSlice';

const ExchangesPage: React.FC = () => {
  const [selectedExchange, setSelectedExchange] = useState<number | null>(null);
  const [showApiForm, setShowApiForm] = useState(false);
  const [apiForm, setApiForm] = useState({
    api_key: '',
    api_secret: '',
    passphrase: '',
  });
  const [showSecrets, setShowSecrets] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);

  const dispatch = useDispatch<AppDispatch>();
  const { exchanges, loading, error } = useSelector((state: RootState) => state.exchange);

  useEffect(() => {
    dispatch(fetchExchanges());
  }, [dispatch]);

  const handleConfigureAPI = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedExchange) {
      try {
        await dispatch(configureExchangeAPI({
          exchange_id: selectedExchange,
          ...apiForm
        })).unwrap();
        setShowApiForm(false);
        setApiForm({ api_key: '', api_secret: '', passphrase: '' });
        setSelectedExchange(null);
      } catch (error) {
        // Error handled by Redux
      }
    }
  };

  const copyToClipboard = (text: string, type: string) => {
    navigator.clipboard.writeText(text);
    setCopied(type);
    setTimeout(() => setCopied(null), 2000);
  };

  const exchangeList = [
    {
      id: 1,
      name: 'Binance',
      logo: '🔵',
      rebate: '40%',
      description: 'World\'s largest cryptocurrency exchange',
      status: 'connected',
      referral_link: 'https://binance.com/ref/123456'
    },
    {
      id: 2,
      name: 'Coinbase',
      logo: '🔵',
      rebate: '35%',
      description: 'Trusted crypto exchange for beginners',
      status: 'not_connected',
      referral_link: 'https://coinbase.com/join/123456'
    },
    {
      id: 3,
      name: 'KuCoin',
      logo: '🔵',
      rebate: '30%',
      description: 'The People\'s Exchange',
      status: 'not_connected',
      referral_link: 'https://kucoin.com/r/123456'
    },
    {
      id: 4,
      name: 'Bybit',
      logo: '🔵',
      rebate: '25%',
      description: 'Professional crypto derivatives exchange',
      status: 'not_connected',
      referral_link: 'https://bybit.com/invite/123456'
    },
    {
      id: 5,
      name: 'OKX',
      logo: '🔵',
      rebate: '30%',
      description: 'Global crypto exchange platform',
      status: 'not_connected',
      referral_link: 'https://okx.com/join/123456'
    },
    {
      id: 6,
      name: 'Kraken',
      logo: '🔵',
      rebate: '20%',
      description: 'Secure cryptocurrency trading platform',
      status: 'not_connected',
      referral_link: 'https://kraken.com/ref/123456'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Exchanges</h1>
          <p className="text-gray-600">
            Connect your exchange accounts to start earning rebates on your trades.
          </p>
        </div>

        {/* Exchange Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {exchangeList.map((exchange, index) => (
            <motion.div
              key={exchange.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="card hover:shadow-lg transition-shadow duration-200"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="text-3xl">{exchange.logo}</div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{exchange.name}</h3>
                    <p className="text-sm text-gray-500">{exchange.description}</p>
                  </div>
                </div>
                <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                  exchange.status === 'connected' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {exchange.status === 'connected' ? 'Connected' : 'Not Connected'}
                </div>
              </div>

              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Rebate Rate</span>
                  <span className="text-lg font-bold text-primary-600">{exchange.rebate}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: exchange.rebate }}
                  ></div>
                </div>
              </div>

              <div className="space-y-3">
                {exchange.status === 'connected' ? (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                      <div className="flex items-center space-x-2">
                        <CheckCircle size={16} className="text-green-600" />
                        <span className="text-sm font-medium text-green-800">API Connected</span>
                      </div>
                      <Settings size={16} className="text-green-600" />
                    </div>
                    <button
                      onClick={() => copyToClipboard(exchange.referral_link, `referral-${exchange.id}`)}
                      className="w-full flex items-center justify-center space-x-2 btn-secondary text-sm"
                    >
                      <Copy size={16} />
                      <span>{copied === `referral-${exchange.id}` ? 'Copied!' : 'Copy Referral Link'}</span>
                    </button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <button
                      onClick={() => {
                        setSelectedExchange(exchange.id);
                        setShowApiForm(true);
                      }}
                      className="w-full btn-primary flex items-center justify-center space-x-2"
                    >
                      <Plus size={16} />
                      <span>Connect API</span>
                    </button>
                    <a
                      href={exchange.referral_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-full btn-secondary flex items-center justify-center space-x-2 text-sm"
                    >
                      <ExternalLink size={16} />
                      <span>Sign Up</span>
                    </a>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>

        {/* API Configuration Modal */}
        {showApiForm && selectedExchange && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-white rounded-2xl p-6 w-full max-w-md"
            >
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  Connect {exchangeList.find(e => e.id === selectedExchange)?.name}
                </h3>
                <button
                  onClick={() => {
                    setShowApiForm(false);
                    setSelectedExchange(null);
                    setApiForm({ api_key: '', api_secret: '', passphrase: '' });
                  }}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleConfigureAPI} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    API Key
                  </label>
                  <div className="relative">
                    <input
                      type={showSecrets ? 'text' : 'password'}
                      value={apiForm.api_key}
                      onChange={(e) => setApiForm(prev => ({ ...prev, api_key: e.target.value }))}
                      className="input-field pr-10"
                      placeholder="Enter your API key"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowSecrets(!showSecrets)}
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    >
                      {showSecrets ? (
                        <EyeOff size={16} className="text-gray-400" />
                      ) : (
                        <Eye size={16} className="text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    API Secret
                  </label>
                  <div className="relative">
                    <input
                      type={showSecrets ? 'text' : 'password'}
                      value={apiForm.api_secret}
                      onChange={(e) => setApiForm(prev => ({ ...prev, api_secret: e.target.value }))}
                      className="input-field pr-10"
                      placeholder="Enter your API secret"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowSecrets(!showSecrets)}
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    >
                      {showSecrets ? (
                        <EyeOff size={16} className="text-gray-400" />
                      ) : (
                        <Eye size={16} className="text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Passphrase (Optional)
                  </label>
                  <input
                    type={showSecrets ? 'text' : 'password'}
                    value={apiForm.passphrase}
                    onChange={(e) => setApiForm(prev => ({ ...prev, passphrase: e.target.value }))}
                    className="input-field"
                    placeholder="Enter your passphrase (if required)"
                  />
                </div>

                {error && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                    <div className="flex items-center space-x-2">
                      <AlertCircle size={16} className="text-red-600" />
                      <p className="text-sm text-red-600">{error}</p>
                    </div>
                  </div>
                )}

                <div className="flex space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowApiForm(false);
                      setSelectedExchange(null);
                      setApiForm({ api_key: '', api_secret: '', passphrase: '' });
                    }}
                    className="flex-1 btn-secondary"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="flex-1 btn-primary disabled:opacity-50"
                  >
                    {loading ? 'Connecting...' : 'Connect'}
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExchangesPage; 