exports.handleChat = async (req, res) => {
  try {
    const { message } = req.body;
    if (!message) return res.status(400).json({ reply: 'Vui lòng nhập tin nhắn' });

    const lower = message.toLowerCase();
    let reply = 'Chào bạn! Tôi là trợ lý ảo Velmora Jewelry. Tôi có thể hỗ trợ tư vấn chọn size nhẫn, gợi ý trang sức phong thuỷ và kiểm tra chính sách bảo hành.';

    if (lower.includes('nhẫn') || lower.includes('size')) {
      reply = 'Để đo size nhẫn chuẩn xác: Bạn dùng một sợi chỉ quấn quanh ngón tay, đo chiều dài mm rồi chia cho 3.14 là ra đường kính lòng nhẫn (Size 5 tương ứng 49mm, Size 6 tương ứng 51mm, Size 7 tương ứng 53mm).';
    } else if (lower.includes('vàng') || lower.includes('chất liệu')) {
      reply = 'Velmora cung cấp các dòng trang sức Bạc S925 mạ Rhodium cao cấp, Vàng 18K và Kim Cương nhân tạo đạt chuẩn quốc tế.';
    } else if (lower.includes('giao hàng') || lower.includes('ship')) {
      reply = 'Velmora miễn phí giao hàng toàn quốc cho tất cả đơn hàng từ 500.000đ. Thời gian giao hàng tiêu chuẩn từ 2 - 4 ngày làm việc.';
    } else if (lower.includes('đổi trả') || lower.includes('bảo hành')) {
      reply = 'Chính sách bảo hành: Bảo hành làm sạch, đánh bóng miễn phí trọn đời và hỗ trợ đổi size trong vòng 7 ngày kể từ khi nhận hàng.';
    }

    res.json({ reply });
  } catch (err) {
    res.status(500).json({ reply: 'Có lỗi xảy ra, vui lòng thử lại sau.' });
  }
};
