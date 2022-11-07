## *GIỚI THIỆU ĐỀ TÀI*
#### I. Định nghĩa
##### 1. Giá trị theo thời gian của tiền
- Theo góc độ tài chính, tiền không ngừng vận động và sinh lời. Giữa tiền với thời gian và rủi ro có quan hệ mật thiết với nhau. Mối quan hệ đó được thể hiện thông qua lãi suất. 
- Đồng tiền nhận được ở các thời điểm khác nhau sẽ có giá trị không giống nhau. Một đồng tiền hôm nay có giá trị hơn một đồng tiền trong tương lai. Giá trị theo thời gian của tiền được cụ thể hóa bởi hai khái niệm cơ bản là giá trị tương lai (FV) và giá trị hiện tại (PV)
##### 2. Lãi suất
- Lãi suất là tỷ lệ phần trăm phát sinh từ giao dịch cho vay giữa các bên. Số tiền này được gọi là tiền lãi mà người vay tiền cần phải trả thêm cho người cho vay
- Lãi suất ngân hàng là tỷ lệ phần trăm quy định trong hợp đồng vay, mượn giữa tiền vốn gửi vào hoặc cho vay với mức lãi suất trong khoảng thời gian nhất định do ngân hàng đưa ra hoặc do bên vay và bên cho vay tự thỏa thuận để phù hợp.
##### 3. Giá trị hiện tại
- Giá trị hiện tại của tiền là giá trị của khoản tiền phát sinh trong tương lai được quy về thời điểm hiện tại (thời điểm gốc) theo một tỷ lệ chiết khấu nhất định
- Thời điểm phát sinh khoản tiền càng xa thời điểm hiện tại thì giá trị hiện tại của khoản tiền càng nhỏ.
- Lãi suất chiết khấu hay tỷ lệ hiện tại hoá càng lớn thì giá trị hiện tại của khoản tiền càng nhỏ.
##### 4. Giá trị tương lai
- Giá trị tương lai của một khoản tiền là giá trị có thể nhận được tại một thời điểm trong tương lai, bao gồm số vốn gốc và toàn bộ tiền lãi tính đến thời điểm đó. Yếu tố ảnh hưởng trực tiếp đến giá trị tương lai của tiền là phương pháp tính lãi
- Trong thực tế, chúng ta thường gặp trường hợp có nhiều khoản tiền phát sinh liên tục theo những khoảng thời gian bằng nhau (điển hình như việc gửi tiết kiệm vào ngân hàng) tạo thành một chuỗi các khoản tiền. Khoảng cách giữa hai khoản tiền phát sinh được tính theo năm, theo quý hoặc theo tháng còn gọi là một kỳ. Tùy theo thời điểm phát sinh các khoản tiền ở đầu kỳ hay cuối kỳ mà người ta sẽ có cách phân biệt và tính toán khác nhau
- Trong đề tài này chúng ta sẽ sử dụng công thức tính giá trị tương lai của dòng tiền đều cuối kỳ khi biết giá trị hiện tại cũng như khoản tiền thanh toán từng kỳ và dựa vào lãi suất thực tế của các ngân hàng hiện nay để tính toán giá trị tương lai của khoản tiền gửi tiết kiệm hoặc vay vốn
> $$ FV = PV(1 + r)^{nper} + PMT \left [\frac{(1 + r)^{nper} - 1}{r} \right ] $$


Trong đó:
- FV: giá trị tương lai sẽ nhận được
- PV: giá trị hiện tại của khoản tiền
- r: lãi suất ngân hàng quy định
- PMT: khoản tiền thanh toán theo từng kỳ cố định
- nper: số kỳ ghép lãi
#### II. Định giá dòng tiền
##### 1. Gửi tiết kiệm

##### 2. Vay vốn
##### 3. Tại sao nên vay vốn/ gửi tiết kiệm

##### 4. Lợi ích của việc dự đoán dòng tiền

#### III. Quy trình thiết kế giao diện định giá dòng tiền

##### 1. Các Package cần sử dụng

##### 2. Các thuật toán liên quan

##### 3. Phương pháp tạo giao diện

#### IV. Kết luận 


The platform of project is [here](https://cashflowexpectation.streamlitapp.com/)

> $$ fv + pv*(1 + rate)^{nper} + pmt \left [\frac{(1 + rate)^{nper} - 1}{rate} \right ] = 0 $$