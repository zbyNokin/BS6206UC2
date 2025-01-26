import pandas as pd


def cluster_peptides_by_gene(peptide_df):
    """
    Cluster peptides by gene and merge highly similar/overlapping sequences.

    Parameters:
    -----------
    peptide_df : pd.DataFrame
        A DataFrame containing at least the following columns:
        - 'Gene Name'
        - 'Peptide'

    Returns:
    --------
    pd.DataFrame
        The original rows with an additional 'Cluster' column, which indicates
        the "longest mother peptide" (or a merged peptide) to which each
        original peptide belongs.
    """

    def get_max_overlap(s1, s2):
        """
        寻找 s1 的后缀和 s2 的前缀的最大重叠长度。
        比如 s1 = ABCDE, s2 = DEFG，则重叠为 'DE'，长度为 2。
        返回最大重叠的长度（int）。
        """
        max_len = min(len(s1), len(s2))
        for length in range(max_len, 0, -1):
            if s1.endswith(s2[:length]):
                return length
        return 0

    def find_merged_sequence(seq1, seq2):
        """
        给定两个肽段，若满足：
        - 彼此有包含关系，则返回较长者。
        - 否则，寻找最大首尾重叠并合并，若能找到非零重叠，则返回合并后的序列。
        - 如果无法合并，返回 None。
        """
        # 1) 若存在包含关系，直接返回更长的
        if seq1 in seq2:
            return seq2
        if seq2 in seq1:
            return seq1

        # 2) 找最大前缀/后缀重叠
        overlap_len_1 = get_max_overlap(seq1, seq2)  # s1 后缀和 s2 前缀
        overlap_len_2 = get_max_overlap(seq2, seq1)  # s2 后缀和 s1 前缀

        # 2.1) 若 seq1 的末尾和 seq2 的开头有最大重叠
        merged_1 = None
        if overlap_len_1 > 0:
            merged_1 = seq1 + seq2[overlap_len_1:]  # 拼接

        # 2.2) 若 seq2 的末尾和 seq1 的开头有最大重叠
        merged_2 = None
        if overlap_len_2 > 0:
            merged_2 = seq2 + seq1[overlap_len_2:]  # 拼接

        # 按照长度或其他规则选一个合并结果
        candidates = [m for m in [merged_1, merged_2] if m]
        if candidates:
            # 先返回最长的合并结果试试
            return max(candidates, key=len)

        # 若没有包含关系、也无法重叠合并，返回 None
        return None

    def merge_peptides(peptides):
        """
        给定同一基因下的所有肽段，聚类成母肽段列表。
        返回一个（可能较少的）母肽段列表，确保其中任何两个都不再能合并。
        """
        # 先按长度从大到小排序
        peptides = sorted(peptides, key=len, reverse=True)
        clusters = []

        for pep in peptides:
            merged_into_existing = False

            for i, cluster_seq in enumerate(clusters):
                merged = find_merged_sequence(cluster_seq, pep)
                if merged is not None:
                    # 若能合并，更新该聚类代表序列
                    clusters[i] = merged
                    merged_into_existing = True
                    break

            if not merged_into_existing:
                # 若无法并入任何已有聚类，新增一个母肽段
                clusters.append(pep)

        return clusters

    # --------------------------------------------------------------
    # 对每个 Gene Name 分组聚合，并对其中的 Peptide 做聚类
    # --------------------------------------------------------------
    output_records = []

    for gene_name, subdf in peptide_df.groupby("Gene Name"):
        # 当前基因下所有肽段列表
        peptides = subdf["Peptide"].tolist()

        # 获得母肽段列表
        mother_peptides = merge_peptides(peptides)

        # 对每条原肽段，匹配到一个合适的母肽段（通常是包含它的那条）
        # 若有多个母肽段都包含它，可以自行决定取第一个或取长度最大的。
        for pep in peptides:
            # 找到所有包含 pep 的母肽段
            candidate_mothers = [m for m in mother_peptides if pep in m]
            if candidate_mothers:
                # 这里简单取长度最大的母肽段
                best_mother = max(candidate_mothers, key=len)
            else:
                # 如果没有任何母肽段包含它（理论上不该出现），就自己当母肽段
                best_mother = pep

            output_records.append({
                "Gene Name": gene_name,
                "Peptide": pep,
                "Cluster": best_mother
            })

    return pd.DataFrame(output_records)
