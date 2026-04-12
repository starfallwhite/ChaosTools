function [x, time] = RungeSolve_electrooptic_chaos_mes(T1, xin, h, N, beta, phi, mes_bits, mes_rate)
% 求解电光延迟混沌系统，信息信号由比特序列经 OOK 调制生成
% 输入:
%   T1       - 延迟时间 (秒)
%   xin      - 初始状态 [x0; y0]
%   h        - 步长 (秒)
%   N        - 迭代步数
%   beta     - 反馈强度
%   phi      - 相位参数
%   mes_bits - 二进制信息序列 (向量，每个元素为 0 或 1)
%   mes_rate - 比特率 (bps)
% 输出:
%   x        - 混沌状态 x 序列 (长度 N)
%   time     - 对应的时间点 (秒)

    x = zeros(1, N);
    x_0 = xin(1);
    y_0 = xin(2);
    n1 = floor(T1 / h);          % 延迟步数

    tou = 25e-12;                % 时间常数 (秒)
    xita = 5e-6;                 % 另一个时间常数 (秒)

    % ---------- 根据比特率和步长生成 OOK 调制波形 ----------
    T_bit = 1 / mes_rate;        % 每个比特持续时间 (秒)
    % 预分配 mes_waveform 数组 (长度 N)
    mes_waveform = zeros(1, N);
    % 默认 OOK 调制: 比特 '1' 映射为幅度 1, '0' 映射为 0
    % 对于每个离散时间点，确定所属比特索引并赋值
    for j = 1:N
        t = j * h;               % 当前时间 (从 h 开始)
        bit_idx = floor(t / T_bit) + 1;   % 对应比特序号 (从1开始)
        if bit_idx <= length(mes_bits)
            mes_waveform(j) = mes_bits(bit_idx);   % OOK 幅度为 1
        else
            % 若比特序列长度不足，后续信号置 0 (可根据需求修改)
            mes_waveform(j) = 0;
        end
    end
    % -----------------------------------------------------

    m = 1;
    for j = 1:N
        time(m) = j * h;

        % 延迟混沌状态 x_delay
        if j <= n1
            x_delay = 20 * (rand(1) - 0.5);   % 初始区间随机值
        else
            x_delay = x(j - n1);
        end

        % 当前时刻的信息信号
        mes_cur = mes_waveform(j);

        % 四阶 Runge-Kutta 求解
        k11 = -(1/tou) * x_0 - (1/(xita*tou)) * y_0 + (beta/tou) * (cos(x_delay - phi) + mes_cur)^2;
        k21 = x_0;

        k12 = -(1/tou) * (x_0 + 0.5*h*k11) - (1/(xita*tou)) * (y_0 + 0.5*h*k21) + (beta/tou) * (cos(x_delay - phi) + mes_cur)^2;
        k22 = x_0 + 0.5*h*k11;

        k13 = -(1/tou) * (x_0 + 0.5*h*k12) - (1/(xita*tou)) * (y_0 + 0.5*h*k22) + (beta/tou) * (cos(x_delay - phi) + mes_cur)^2;
        k23 = x_0 + 0.5*h*k12;

        k14 = -(1/tou) * (x_0 + h*k13) - (1/(xita*tou)) * (y_0 + h*k23) + (beta/tou) * (cos(x_delay - phi) + mes_cur)^2;
        k24 = x_0 + h*k13;

        x_0 = x_0 + h * (k11 + 2*k12 + 2*k13 + k14) / 6;
        y_0 = y_0 + h * (k21 + 2*k22 + 2*k23 + k24) / 6;

        x(j) = x_0;
        m = m + 1;
    end
end