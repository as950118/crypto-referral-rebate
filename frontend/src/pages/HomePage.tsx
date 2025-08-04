import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowRight, 
  CheckCircle, 
  TrendingUp, 
  Shield, 
  Zap, 
  Users, 
  DollarSign,
  BarChart3,
  Wallet,
  Star
} from 'lucide-react';

const HomePage: React.FC = () => {
  const features = [
    {
      icon: TrendingUp,
      title: 'Maximum Rebates',
      description: 'Get up to 40% back on your trading fees with our competitive rebate rates.'
    },
    {
      icon: Shield,
      title: 'Secure & Reliable',
      description: 'Bank-grade security with encrypted API connections and secure data handling.'
    },
    {
      icon: Zap,
      title: 'Instant Setup',
      description: 'Connect your exchange accounts in minutes and start earning immediately.'
    },
    {
      icon: Users,
      title: 'Multi-Exchange',
      description: 'Support for all major exchanges including Binance, Coinbase, KuCoin, and more.'
    }
  ];

  const stats = [
    { label: 'Active Users', value: '10,000+', icon: Users },
    { label: 'Total Rebates', value: '$2.5M+', icon: DollarSign },
    { label: 'Supported Exchanges', value: '15+', icon: Wallet },
    { label: 'Success Rate', value: '99.9%', icon: Star }
  ];

  const exchanges = [
    { name: 'Binance', logo: '🔵', rebate: '40%' },
    { name: 'Coinbase', logo: '🔵', rebate: '35%' },
    { name: 'KuCoin', logo: '🔵', rebate: '30%' },
    { name: 'Bybit', logo: '🔵', rebate: '25%' },
    { name: 'OKX', logo: '🔵', rebate: '30%' },
    { name: 'Kraken', logo: '🔵', rebate: '20%' }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 text-white">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
                Maximize Your
                <span className="block text-yellow-300">Crypto Profits</span>
              </h1>
              <p className="text-xl md:text-2xl text-primary-100 mb-8 leading-relaxed">
                Get up to 40% back on trading fees from major exchanges. 
                Connect your accounts and start earning today.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  to="/register"
                  className="bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-bold py-4 px-8 rounded-lg text-lg transition-colors duration-200 flex items-center justify-center space-x-2"
                >
                  <span>Start Earning Now</span>
                  <ArrowRight size={20} />
                </Link>
                <Link
                  to="/login"
                  className="border-2 border-white hover:bg-white hover:text-primary-700 text-white font-bold py-4 px-8 rounded-lg text-lg transition-colors duration-200"
                >
                  Sign In
                </Link>
              </div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="relative"
            >
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-yellow-400 rounded-lg flex items-center justify-center">
                        <DollarSign size={24} className="text-gray-900" />
                      </div>
                      <div>
                        <p className="text-sm text-primary-200">Total Rebates</p>
                        <p className="text-2xl font-bold">$12,450.67</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-green-400">+15.3%</p>
                      <p className="text-xs text-primary-200">This month</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white/10 rounded-lg p-4">
                      <p className="text-sm text-primary-200">Monthly Rebates</p>
                      <p className="text-xl font-bold">$2,340.12</p>
                    </div>
                    <div className="bg-white/10 rounded-lg p-4">
                      <p className="text-sm text-primary-200">Connected Exchanges</p>
                      <p className="text-xl font-bold">4</p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="text-center"
                >
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Icon size={24} className="text-primary-600" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{stat.value}</h3>
                  <p className="text-gray-600">{stat.label}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose CryptoRebate?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We provide the highest rebate rates in the industry with unmatched security and ease of use.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200"
                >
                  <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                    <Icon size={24} className="text-primary-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                  <p className="text-gray-600">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Exchanges Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Supported Exchanges
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Connect your favorite exchanges and start earning rebates immediately.
            </p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {exchanges.map((exchange, index) => (
              <motion.div
                key={exchange.name}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-gray-50 rounded-xl p-6 text-center hover:bg-gray-100 transition-colors duration-200"
              >
                <div className="text-4xl mb-3">{exchange.logo}</div>
                <h3 className="font-semibold text-gray-900 mb-2">{exchange.name}</h3>
                <p className="text-primary-600 font-bold">{exchange.rebate} Rebate</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-primary-600 to-primary-800 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Ready to Start Earning?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Join thousands of traders who are already maximizing their profits with CryptoRebate.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-bold py-4 px-8 rounded-lg text-lg transition-colors duration-200 flex items-center justify-center space-x-2"
              >
                <span>Get Started Free</span>
                <ArrowRight size={20} />
              </Link>
              <Link
                to="/login"
                className="border-2 border-white hover:bg-white hover:text-primary-700 text-white font-bold py-4 px-8 rounded-lg text-lg transition-colors duration-200"
              >
                Sign In
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default HomePage; 