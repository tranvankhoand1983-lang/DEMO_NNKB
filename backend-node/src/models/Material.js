const mongoose = require('mongoose');

const materialSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  slug: { type: String, required: true, unique: true },
  name: { type: String, required: true }
});

module.exports = mongoose.model('Material', materialSchema, 'materials');
