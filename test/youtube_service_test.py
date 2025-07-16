from app.external_service.external_platform.Youtube import youtube_service

def getStatisticsInfoBatch_test():
    result = youtube_service.getStatisticsInfoBatch(["N3_VW5xKtmQ", "zfjFsmedW5s"])
    for video_id, stats in result.items():
        print(f"Video ID: {video_id}, Statistics: {stats}")

if __name__ == "__main__":
    getStatisticsInfoBatch_test()