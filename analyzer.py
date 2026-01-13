import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def read_csv_handle_time(csv_path: str):
    df = pd.read_csv(csv_path, skipinitialspace=True)

    sec = df["sec"].to_numpy()
    nsec = df["nsec"].to_numpy()
    time = sec + (nsec / 10**9)
    time = time - time[0]
    df = df.drop(columns=["sec", "nsec"])
    df["time"] = time
    df = df[["time"] + [col for col in df.columns if col != "time"]]
    return df


def windowed_rms_from_csv(csv_path: str, window_sec: float | int, value_p: str):

    df = read_csv_handle_time(csv_path)

    time = df["time"].to_numpy()

    value = df[value_p].to_numpy()

    results = []

    start_time = time[0]
    end_time = time[-1]

    t0 = start_time
    while t0 + window_sec <= end_time:
        t1 = t0 + window_sec

        # Indices within window
        mask = (time >= t0) & (time <= t1)
        t_win = time[mask]
        v_win = value[mask]

        if len(t_win) < 2:
            t0 = t1
            continue

        # Time deltas
        dt = np.diff(t_win)

        # Midpoint rule for v^2 integral
        v_sq_mid = (v_win[:-1] ** 2 + v_win[1:] ** 2) / 2
        integral = np.sum(v_sq_mid * dt)

        rms = np.sqrt(integral / window_sec)

        results.append({"window_start": t0, "window_end": t1, "rms": rms})

        t0 = t1

    def rms_v_itr():
        for result in results:
            yield result["rms"]

    nz_rms = list(filter(lambda x: x != 0, rms_v_itr()))

    avg_nz_rms = sum(nz_rms) / len(nz_rms)

    results[0]["rms_mean"] = np.mean(nz_rms)

    results[0]["nz_rms_mean"] = avg_nz_rms

    q1 = np.quantile(nz_rms, 0.25)
    q2 = np.quantile(nz_rms, 0.5)
    q3 = np.quantile(nz_rms, 0.75)

    results[0]["nz_rms_q0"] = min(nz_rms)
    results[0]["nz_rms_q1"] = q1
    results[0]["nz_rms_q2"] = q2
    results[0]["nz_rms_q3"] = q3
    results[0]["nz_rms_q4"] = max(nz_rms)

    return pd.DataFrame(results)


def create_boxplot(
    fname: str,
    values: list[np.ndarray],
    w_values: list[int | float],
    header: str,
    strip_zeros=False,
):
    plt.figure()
    for idx, arr in enumerate(values):
        values[idx] = np.abs(arr)
        if strip_zeros:
            arr = values[idx]
            arr_no_zeros = arr[arr != 0]
            values[idx] = arr_no_zeros

    plt.boxplot(values, showmeans=True)
    ticks = [1]
    labels = ["Raw"]
    for w in w_values:
        ticks.append(ticks[-1] + 1)
        labels.append(f"w={w} sec")

    plt.xticks(ticks, labels)
    plt.ylabel("Current (A)")
    plt.title(f"RMS Comparison for {header} {'' if not strip_zeros else " (nz)"}")
    plt.savefig(fname)


def main():
    csv_files = [
        "hopper_act.info.csv",
        "hopper_belt.info.csv",
        "track_left.info.csv",
        "track_right.info.csv",
        "trencher.info.csv",
    ]

    for csv_file in csv_files:
        excel_file = f"./out/{csv_file}_analyzed.xlsx"
        with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
            workbook = writer.book

            worksheet = workbook.add_worksheet("raw")
            writer.sheets["raw"] = worksheet
            raw = read_csv_handle_time(csv_file)
            raw.to_excel(writer, sheet_name="raw", startrow=0, startcol=0, index=False)

            for value_p in ["supply_current", "output_current"]:
                values = [raw[value_p].to_numpy()]
                W_VALUES = (0.1, 1, 3, 5, 10, 60)
                for w in W_VALUES:

                    df_rms = windowed_rms_from_csv(csv_file, w, value_p)
                    values.append(df_rms["rms"].to_numpy())

                    sheet_name = f"win_sz={w}sec, p={value_p}"
                    worksheet = workbook.add_worksheet(sheet_name)
                    writer.sheets[sheet_name] = worksheet
                    df_rms.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        startrow=0,
                        startcol=0,
                        index=False,
                    )
                create_boxplot(
                    f"out/{csv_file}_{value_p}_boxplot.png", values, W_VALUES, value_p
                )
                create_boxplot(
                    f"out/{csv_file}_{value_p}_nz_boxplot.png",
                    values,
                    W_VALUES,
                    value_p,
                    strip_zeros=True,
                )


if __name__ == "__main__":
    if not os.path.exists("./out"):
        os.mkdir("./out")
    main()
